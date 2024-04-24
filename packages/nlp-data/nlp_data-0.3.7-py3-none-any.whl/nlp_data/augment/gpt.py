from enum import Enum
from openai import OpenAI
import os
from ..document import NLUDocList, NLUDoc, APIDocList, APIDoc, DialogueDoc, DialogueDocList, APIParam
from ..document.nlu import Entity
from ..document.dialogue import Message
from docarray import DocList
from pydantic import validate_arguments
from tqdm import tqdm, trange
from wasabi import msg
from typing import List


class Localism(str, Enum):
    """方言
    """
    guangdong: str = '广东话'
    sichuan: str = '四川话'
    english: str = '英语'
    
    
class GPTAugmentor:
    """基于ChatGPT的数据增强器
    """
    def __init__(self, 
                 api_key: str = None,
                 model: str = 'gpt-3.5-turbo-0613',
                 api_base: str = 'https://us-pachira-aiproxy.pachira.cn/v1'):
        
        api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError('请设置OPENAI_API_KEY环境变量')
        self.chat_model = model
        self.client = OpenAI(api_key=api_key, base_url=api_base)
        
    @validate_arguments
    def get_chatgpt_response(self, query: str, system: str = None) -> str:
        messages = [{"role": "user", "content": query}]
        if system:
            messages = [{"role": "system", "content": system}] + messages
            
        chat_completion = self.client.chat.completions.create(model=self.chat_model, messages=messages)
        return chat_completion.choices[0].message.content

    @validate_arguments
    def augment_nlu_by_localism(self, docs: NLUDocList,  localism: Localism = Localism.guangdong, max_retry: int = 5):
        """利用chatgpt数据增强不同方言的表述

        Args:
            docs (NLUDocList): 原始文档,如果doc.abnf_output为None,则不会增强.
            localism (Localism, optional): 方言. Defaults to Localism.guangdong.

        Returns:
            Tuple[NLUDocList, NLUDocList] : 增强后的文档和增强失败的文档
        """
        prompt = "将下面的标注文本转换为{}表述形式,如果有B,I等实体序列标注符号,要求保留B,I标注符号,且要标注正确.文本:".format(localism.value)
        system = "你是一个数据增强器,你要根据用户的要求对数据进行增强."
        new_docs = NLUDocList(docs=[])

        for i in tqdm(range(len(docs))):
            doc: NLUDoc = docs[i]
            retry = 0
            while retry < max_retry:
                try:
                    query = prompt + "\n{}".format(doc.abnf_output)
                    response = self.get_chatgpt_response(query=query, system=system)
                    if localism == '英语':
                        lang = 'en'
                    else:
                        lang = 'zh'
                    new_doc = NLUDoc.from_abnf_output_line(line=response, domain=doc.domain.text, intention=doc.intention.text, lang=lang)
                    assert len(doc.slots) == len(new_doc.slots)
                    new_docs.append(new_doc)
                    retry = max_retry
                except Exception as e:
                    print(e)
                    retry = retry + 1
                    msg.fail(f'augment doc {doc.id} fail, retry: {retry} / {max_retry}')
        msg.good(f'augment {len(new_docs)} / {len(docs)} docs success')
        return new_docs
    
    
    @validate_arguments
    def augment_dialogue(self, docs: DialogueDocList, num_docs: int = 2, max_retry: int = 5):
        """对已有多轮对话数据进行模仿,生成新的多轮对话数据

        Args:
            docs (DialogueDocList): 已有的多轮对话数据.
            num_docs (int, optional): 对每个已有doc生成的新doc的数量. Defaults to 2.
            max_retry (int, optional): 调用chatgpt错误最大重试次数. Defaults to 5.

        Returns:
            DialogueDocList: 新生成的多轮对话数据
        """
        new_docs = DialogueDocList()
        for doc in tqdm(docs):
            for i in range(num_docs):
                retry = 0
                while retry < max_retry:
                    try:
                        prompt = ""
                        if doc.theme:
                            prompt += f"主题: {doc.theme}\n"
                        if doc.situation:
                            prompt += f"情景: {doc.situation}\n"
                        prompt += "多轮对话: \n"
                        for message in doc.conversation:
                            prompt += f"{message.role}: {message.content}\n"
                        prompt += "请根据上面的对话的内容,重新生成跟以上对话情景和主题一致的对话,不要跟原来对话一样,询问内容的顺序也可以不一致,可以在该情景下想象新的对话内容,仅用以下格式返回: User: xxx, Bot: xxx"
                        response = self.get_chatgpt_response(prompt)
                        new_doc = DialogueDoc()
                        new_doc.theme = doc.theme
                        new_doc.situation = doc.situation
                        turns = []
                        for turn in response.split('\n'):
                            turn = turn.strip()
                            if len(turn) > 0:
                                turns.append(turn)
                        assert len(turns) % 2 == 0
                        for i in range(0, len(turns), 2):
                            assert turns[i].startswith('User:')
                            assert turns[i+1].startswith('Bot:')
                            message = Message(role='user', content=turns[i][5:])
                            new_doc.conversation.append(message)
                            message = Message(role='assistant', content=turns[i+1][5:])
                            new_doc.conversation.append(message)
                        new_docs.append(new_doc)
                        retry = max_retry
                    except Exception:
                        msg.fail(f'augment doc {doc.id} fail')
                        retry += 1
        return new_docs
    
    
    
    @validate_arguments
    def complete_api_docs(self, docs: APIDocList, max_retry: int = 5):
        """补充API文档的描述

        Args:
            docs (APIDocList): API文档列表

        Returns:
            _type_: APIDocList
        """
        complete_docs = APIDocList()
        for doc in tqdm(docs):
            retry = 0
            while retry < max_retry:
                try:
                    if not doc.description or doc.description == 'nan' or doc.description == 'None' or doc.description == 'none':
                        prompt = "API名称:{},API参数:{}, 请根据上面的信息给出API的描述,只返回描述:\n\n".format(doc.name, doc.params.name)
                        description = self.get_chatgpt_response(prompt).strip()
                        new_doc = APIDoc(name=doc.name, description=description)
                    else:
                        new_doc = doc.copy()
                    for param in doc.params:
                        if not param.description or param.description == 'nan' or param.description == 'None' or param.description == 'none':
                            prompt = "{}是API{}的参数名称,API{}的描述如下:{} 给出{}参数描述,要求1.要求参数的描述尽可能简洁. 2.要求要举例说明参数. 3.要求只返回该参数的描述:\n\n".format(param.name, doc.name, doc.name, doc.description, param.name)
                            param_description = self.get_chatgpt_response(prompt).strip()
                            param = APIParam(name=param.name, description=param_description, type=param.type, required=param.required)
                            new_doc.params.append(param)
                        else:
                            new_doc.params.append(param.copy())
                            
                    complete_docs.append(new_doc)
                    retry = max_retry
                except:
                    msg.fail(f'complete doc {doc.id} fail')
                    retry += 1
        return complete_docs
    
    
    # 基于gpt生成多轮对话数据
    def generate_dialogue_docs(self, theme: str, situation: str, num_docs: int = 5, max_retry: int = 5):
        """跟定一个主题,生成多轮对话数据

        Args:
            theme (str): 对话主题.
            num_docs (int, optional): 生成的文档数. Defaults to 5.
        """
        docs = DialogueDocList()
        for j in trange(num_docs):
            retry = 0
            while retry < max_retry:
                try:
                    prompt = f"帮我生成一个在{situation}情景下,关于{theme}的多轮对话, 仅用以下格式返回: User: xxx, Bot: xxx"
                    response = self.get_chatgpt_response(prompt)
                    doc = DialogueDoc()
                    doc.theme = theme
                    doc.situation = situation
                    turns = []
                    for turn in response.split('\n'):
                        if len(turn) > 0:
                            turns.append(turn)
                    assert len(turns) % 2 == 0
                    for i in range(0, len(turns), 2):
                        assert turns[i].startswith('User:')
                        assert turns[i+1].startswith('Bot:')
                        message = Message(role='user', content=turns[i][5:])
                        doc.conversation.append(message)
                        message = Message(role='assistant', content=turns[i+1][5:])
                        doc.conversation.append(message)
                    docs.append(doc)
                    retry = max_retry
                except Exception:  # noqa: E722
                    retry += 1
                    msg.fail(f'generate doc {j} fail. retry {retry}')
                
        return docs
    
    def translate_nlu_en(self, docs: NLUDocList) -> NLUDocList:
        """将文档的文本翻译为英文
        """
        translated_docs = NLUDocList()
        template = "将文本翻译为英文: {text}"
        for doc in tqdm(docs):
            prompt = template.format(text=doc.text)
            translated_text = self.get_chatgpt_response(query=prompt)
            translated_doc = NLUDoc(text=translated_text)
            if doc.domain:
                translated_doc.set_domain(text=doc.domain.text)
            if doc.intention:
                translated_doc.set_intention(text=doc.intention.text)
            translated_docs.append(translated_doc)
        return translated_docs
    
    def augment_nlu_prior_ents(self, docs: NLUDocList, prior_ent_labels: List[str], max_retry: int = 5) -> NLUDocList:
        """为nlu文档添加先验的实体信息,当做外部词典信息的替代方案.
        """
        labels = set(docs.traverse_flat("slots__label"))
        for label in prior_ent_labels:
            if label not in labels:
                raise ValueError(f"prior ent label {label} not in docs. all labels: {labels}")
        prompt_template = """找出下面的文本中的实体信息,并标注实体类型,实体类型包括: {ent_labels}.
        文本: 
        {text}
        
        要求:
        
        1. 以下面的格式返回: [(实体1, 实体1类型), (实体2, 实体2类型), ...]
        2. 如果没有实体,只返回空列表`[]`,不要返回无用的信息.
        """
        for doc in tqdm(docs):
            prompt = prompt_template.format(ent_labels=prior_ent_labels, text=doc.text)
            retry = 0
            while retry < max_retry:
                try:
                    response = self.get_chatgpt_response(query=prompt)
                    ents = eval(response)
                    if len(ents) == 0:
                        doc.prior_ents = DocList[Entity]()
                    else:
                        for ent, label in ents:
                            doc.set_prior_ent(text=ent, label=label)
                    retry = max_retry
                except Exception as e:
                    print(e)
                    msg.fail(f"augment doc {doc.id} fail, retry: {retry} / {max_retry}")
                    retry += 1
        return docs