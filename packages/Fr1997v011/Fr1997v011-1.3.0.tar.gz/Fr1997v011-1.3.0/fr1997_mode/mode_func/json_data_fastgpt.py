import time

false = False
true = True


def json_app_update(dataset_id, cue_word):
    return {
        "modules": [{
            "name": "系统配置",
            "flowType": "userGuide",
            "inputs": [{
                "key": "welcomeText",
                "type": "hidden",
                "label": "core.app.Welcome Text",
                "value": "你好，我是电影《星际穿越》 AI 助手，有什么可以帮助你的？\n[导演是谁]\n[剧情介绍]\n[票房分析]"
            }, {
                "key": "variables",
                "type": "hidden",
                "label": "core.app.Chat Variable",
                "value": []
            }, {
                "key": "questionGuide",
                "type": "hidden",
                "label": "core.app.Question Guide",
                "value": false
            }, {
                "key": "tts",
                "type": "hidden",
                "label": "",
                "value": {
                    "type": "web"
                }
            }, {
                "key": "whisper",
                "type": "hidden",
                "label": "",
                "value": {
                    "open": false,
                    "autoSend": false,
                    "autoTTSResponse": false
                }
            }],
            "outputs": [],
            "position": {
                "x": 447.98520778293346,
                "y": 721.4016845336229
            },
            "moduleId": "userGuide"
        }, {
            "moduleId": "userChatInput",
            "name": "core.module.template.Chat entrance",
            "intro": "当用户发送一个内容后，流程将会从这个模块开始执行。",
            "avatar": "/imgs/module/userChatInput.svg",
            "flowType": "questionInput",
            "position": {
                "x": 324.81436595478294,
                "y": 1527.0012457753612
            },
            "inputs": [{
                "key": "userChatInput",
                "type": "systemInput",
                "valueType": "string",
                "label": "core.module.input.label.user question",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }],
            "outputs": [{
                "key": "userChatInput",
                "label": "core.module.input.label.user question",
                "type": "source",
                "valueType": "string",
                "targets": [{
                    "moduleId": "0voh5n",
                    "key": "userChatInput"
                }]
            }]
        }, {
            "moduleId": "63toub",
            "name": "AI 对话",
            "intro": "AI 大模型对话",
            "avatar": "/imgs/module/AI.png",
            "flowType": "chatNode",
            "showStatus": true,
            "position": {
                "x": 1962.4010270586014,
                "y": 1026.9105717680477
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "model",
                "type": "settingLLMModel",
                "label": "core.module.input.label.aiModel",
                "required": true,
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "gpt-3.5-turbo",
                "connected": false
            }, {
                "key": "temperature",
                "type": "hidden",
                "label": "",
                "value": 0,
                "valueType": "number",
                "min": 0,
                "max": 10,
                "step": 1,
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "maxToken",
                "type": "hidden",
                "label": "",
                "value": 2000,
                "valueType": "number",
                "min": 100,
                "max": 4000,
                "step": 50,
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "isResponseAnswerText",
                "type": "hidden",
                "label": "",
                "value": true,
                "valueType": "boolean",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "quoteTemplate",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "quotePrompt",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "systemPrompt",
                "type": "textarea",
                "max": 3000,
                "valueType": "string",
                "label": "core.ai.Prompt",
                "description": "core.app.tip.chatNodeSystemPromptTip",
                "placeholder": "core.app.tip.chatNodeSystemPromptTip",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": false,
                "value": cue_word
            }, {
                "key": "history",
                "type": "numberInput",
                "label": "core.module.input.label.chat history",
                "required": true,
                "min": 0,
                "max": 30,
                "valueType": "chatHistory",
                "value": 6,
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "userChatInput",
                "type": "custom",
                "label": "",
                "required": true,
                "valueType": "string",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "toolDescription": "用户问题",
                "connected": true
            }, {
                "key": "quoteQA",
                "type": "settingDatasetQuotePrompt",
                "label": "知识库引用",
                "description": "core.module.Dataset quote.Input description",
                "valueType": "datasetQuote",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }],
            "outputs": [{
                "key": "userChatInput",
                "label": "core.module.input.label.user question",
                "type": "hidden",
                "valueType": "string",
                "targets": []
            }, {
                "key": "history",
                "label": "core.module.output.label.New context",
                "description": "core.module.output.description.New context",
                "valueType": "chatHistory",
                "type": "source",
                "targets": []
            }, {
                "key": "answerText",
                "label": "core.module.output.label.Ai response content",
                "description": "core.module.output.description.Ai response content",
                "valueType": "string",
                "type": "source",
                "targets": []
            }, {
                "key": "finish",
                "label": "core.module.output.label.running done",
                "description": "core.module.output.description.running done",
                "valueType": "boolean",
                "type": "source",
                "targets": []
            }]
        }, {
            "moduleId": "0voh5n",
            "name": "知识库搜索",
            "intro": "调用“语义检索”和“全文检索”能力，从“知识库”中查找可能与问题相关的参考内容",
            "avatar": "/imgs/module/db.png",
            "flowType": "datasetSearchNode",
            "showStatus": true,
            "position": {
                "x": 1098.245668870126,
                "y": 1166.7285333032098
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "datasets",
                "type": "selectDataset",
                "label": "core.module.input.label.Select dataset",
                "value": [{
                    "datasetId": dataset_id,
                    "vectorModel": {
                        "model": "text-embedding-ada-002",
                        "name": "Embedding-2",
                        "inputPrice": 0,
                        "outputPrice": 0,
                        "defaultToken": 700,
                        "maxToken": 3000,
                        "weight": 100,
                        "defaultConfig": {}
                    }
                }],
                "valueType": "selectDataset",
                "list": [],
                "required": true,
                "showTargetInApp": false,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "similarity",
                "type": "selectDatasetParamsModal",
                "label": "",
                "value": 0.4,
                "valueType": "number",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "limit",
                "type": "hidden",
                "label": "",
                "value": 1500,
                "valueType": "number",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "searchMode",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "embedding",
                "connected": false
            }, {
                "key": "usingReRank",
                "type": "hidden",
                "label": "",
                "valueType": "boolean",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": false,
                "connected": false
            }, {
                "key": "datasetSearchUsingExtensionQuery",
                "type": "hidden",
                "label": "",
                "valueType": "boolean",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": true,
                "connected": false
            }, {
                "key": "datasetSearchExtensionModel",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "datasetSearchExtensionBg",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "",
                "connected": false
            }, {
                "key": "userChatInput",
                "type": "custom",
                "label": "",
                "required": true,
                "valueType": "string",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "toolDescription": "需要检索的内容",
                "connected": true
            }],
            "outputs": [{
                "key": "userChatInput",
                "label": "core.module.input.label.user question",
                "type": "hidden",
                "valueType": "string",
                "targets": [{
                    "moduleId": "63toub",
                    "key": "userChatInput"
                }]
            }, {
                "key": "isEmpty",
                "label": "core.module.output.label.Search result empty",
                "type": "source",
                "valueType": "boolean",
                "targets": []
            }, {
                "key": "unEmpty",
                "label": "core.module.output.label.Search result not empty",
                "type": "source",
                "valueType": "boolean",
                "targets": []
            }, {
                "key": "quoteQA",
                "label": "core.module.Dataset quote.label",
                "type": "source",
                "valueType": "datasetQuote",
                "targets": [{
                    "moduleId": "63toub",
                    "key": "quoteQA"
                }]
            }]
        }],
        "type": "simple"
    }


def json_app_create(member_id):
    avatar = "/icon/logo.svg"
    time_data = time.strftime("%Y%m%d", time.localtime(int(time.time())))
    return {
        "avatar": avatar,
        "name": f'{time_data}-{int(time.time())}-{member_id}',
        "type": "advanced",
        "modules": [{
            "moduleId": "7z5g5h",
            "name": "core.module.template.Chat entrance",
            "flowType": "questionInput",
            "position": {
                "x": -269.50851681351924,
                "y": 1657.6123698022448
            },
            "inputs": [{
                "key": "userChatInput",
                "type": "systemInput",
                "valueType": "string",
                "label": "core.module.input.label.user question",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }],
            "outputs": [{
                "key": "userChatInput",
                "label": "core.module.input.label.user question",
                "type": "source",
                "valueType": "string",
                "targets": [{
                    "moduleId": "remuj3",
                    "key": "userChatInput"
                }]
            }]
        }, {
            "moduleId": "remuj3",
            "name": "问题分类",
            "flowType": "classifyQuestion",
            "showStatus": true,
            "position": {
                "x": 446.8376904635288,
                "y": 1055.101958605594
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "model",
                "type": "selectLLMModel",
                "valueType": "string",
                "label": "core.module.input.label.Classify model",
                "required": true,
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "gpt-3.5-turbo",
                "connected": false
            }, {
                "key": "systemPrompt",
                "type": "textarea",
                "valueType": "string",
                "label": "core.module.input.label.Background",
                "description": "core.module.input.description.Background",
                "placeholder": "core.module.input.placeholder.Classify background",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "value": "",
                "connected": false
            }, {
                "key": "history",
                "type": "numberInput",
                "label": "core.module.input.label.chat history",
                "required": true,
                "min": 0,
                "max": 30,
                "valueType": "chatHistory",
                "value": 6,
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "userChatInput",
                "type": "custom",
                "label": "",
                "required": true,
                "valueType": "string",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }, {
                "key": "agents",
                "type": "custom",
                "valueType": "any",
                "label": "",
                "value": [{
                    "value": "关于电影《星际穿越》的问题",
                    "key": "wqre"
                }, {
                    "value": "打招呼、问候等问题",
                    "key": "sdfa"
                }, {
                    "value": "其他问题",
                    "key": "oy1c"
                }],
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }],
            "outputs": [{
                "key": "wqre",
                "label": "",
                "type": "hidden",
                "targets": [{
                    "moduleId": "fljhzy",
                    "key": "switch"
                }]
            }, {
                "key": "sdfa",
                "label": "",
                "type": "hidden",
                "targets": [{
                    "moduleId": "a99p6z",
                    "key": "switch"
                }]
            }, {
                "key": "oy1c",
                "label": "",
                "type": "hidden",
                "targets": [{
                    "moduleId": "iejcou",
                    "key": "switch"
                }]
            }, {
                "key": "agex",
                "label": "",
                "type": "hidden",
                "targets": []
            }, {
                "key": "userChatInput",
                "label": "core.module.input.label.user question",
                "type": "hidden",
                "valueType": "string",
                "targets": [{
                    "moduleId": "fljhzy",
                    "key": "userChatInput"
                }]
            }]
        }, {
            "moduleId": "a99p6z",
            "name": "指定回复",
            "flowType": "answerNode",
            "position": {
                "x": 1259.0649974848573,
                "y": 1681.4596399262844
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }, {
                "key": "text",
                "type": "textarea",
                "valueType": "any",
                "label": "core.module.input.label.Response content",
                "description": "core.module.input.description.Response content",
                "placeholder": "core.module.input.description.Response content",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "value": "你好，有什么可以帮助你的？",
                "connected": false
            }],
            "outputs": [{
                "key": "finish",
                "label": "core.module.output.label.running done",
                "description": "core.module.output.description.running done",
                "valueType": "boolean",
                "type": "source",
                "targets": []
            }]
        }, {
            "moduleId": "iejcou",
            "name": "指定回复",
            "flowType": "answerNode",
            "position": {
                "x": 1294.6389464245608,
                "y": 2192.8473001117936
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }, {
                "key": "text",
                "type": "textarea",
                "valueType": "any",
                "label": "core.module.input.label.Response content",
                "description": "core.module.input.description.Response content",
                "placeholder": "core.module.input.description.Response content",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "value": "你好，我仅能回答电影《星际穿越》相关问题，请问你有什么问题么？",
                "connected": false
            }],
            "outputs": [{
                "key": "finish",
                "label": "core.module.output.label.running done",
                "description": "core.module.output.description.running done",
                "valueType": "boolean",
                "type": "source",
                "targets": []
            }]
        }, {
            "moduleId": "nlfwkc",
            "name": "AI 对话",
            "flowType": "chatNode",
            "showStatus": true,
            "position": {
                "x": 2043.3729922717066,
                "y": 1169.5918756185272
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }, {
                "key": "model",
                "type": "selectLLMModel",
                "label": "core.module.input.label.aiModel",
                "required": true,
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "gpt-3.5-turbo",
                "connected": false
            }, {
                "key": "temperature",
                "type": "hidden",
                "label": "",
                "value": 0,
                "valueType": "number",
                "min": 0,
                "max": 10,
                "step": 1,
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "maxToken",
                "type": "hidden",
                "label": "",
                "value": 2000,
                "valueType": "number",
                "min": 100,
                "max": 4000,
                "step": 50,
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "isResponseAnswerText",
                "type": "hidden",
                "label": "",
                "value": true,
                "valueType": "boolean",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "quoteTemplate",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "quotePrompt",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "systemPrompt",
                "type": "textarea",
                "label": "core.ai.Prompt",
                "max": 300,
                "valueType": "string",
                "description": "core.app.tip.chatNodeSystemPromptTip",
                "placeholder": "core.app.tip.chatNodeSystemPromptTip",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "value": "",
                "connected": false
            }, {
                "key": "history",
                "type": "numberInput",
                "label": "core.module.input.label.chat history",
                "required": true,
                "min": 0,
                "max": 30,
                "valueType": "chatHistory",
                "value": 6,
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "userChatInput",
                "type": "custom",
                "label": "",
                "required": true,
                "valueType": "string",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }, {
                "key": "quoteQA",
                "type": "target",
                "label": "知识库引用",
                "description": "core.module.Dataset quote.Input description",
                "valueType": "datasetQuote",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }],
            "outputs": [{
                "key": "answerText",
                "label": "core.module.output.label.Ai response content",
                "description": "core.module.output.description.Ai response content",
                "valueType": "string",
                "type": "source",
                "targets": []
            }, {
                "key": "finish",
                "label": "core.module.output.label.running done",
                "description": "core.module.output.description.running done",
                "valueType": "boolean",
                "type": "source",
                "targets": []
            }, {
                "key": "history",
                "label": "core.module.output.label.New context",
                "description": "core.module.output.description.New context",
                "valueType": "chatHistory",
                "type": "source",
                "targets": []
            }, {
                "key": "userChatInput",
                "label": "core.module.input.label.user question",
                "type": "hidden",
                "valueType": "string",
                "targets": []
            }]
        }, {
            "moduleId": "fljhzy",
            "name": "core.module.template.Dataset search",
            "flowType": "datasetSearchNode",
            "showStatus": true,
            "position": {
                "x": 1307.1997559129973,
                "y": 908.9246215273222
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }, {
                "key": "datasets",
                "type": "selectDataset",
                "label": "core.module.input.label.Select dataset",
                "value": [],
                "valueType": "selectDataset",
                "list": [],
                "required": true,
                "showTargetInApp": false,
                "showTargetInPlugin": true,
                "connected": false
            }, {
                "key": "similarity",
                "type": "selectDatasetParamsModal",
                "label": "",
                "value": 0.8,
                "valueType": "number",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "limit",
                "type": "hidden",
                "label": "",
                "value": 1500,
                "valueType": "number",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "searchMode",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "embedding",
                "connected": false
            }, {
                "key": "usingReRank",
                "type": "hidden",
                "label": "",
                "valueType": "boolean",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": false,
                "connected": false
            }, {
                "key": "datasetSearchUsingExtensionQuery",
                "type": "hidden",
                "label": "",
                "valueType": "boolean",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": true,
                "connected": false
            }, {
                "key": "datasetSearchExtensionModel",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "gpt-3.5-turbo",
                "connected": false
            }, {
                "key": "datasetSearchExtensionBg",
                "type": "hidden",
                "label": "",
                "valueType": "string",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "",
                "connected": false
            }, {
                "key": "userChatInput",
                "type": "custom",
                "label": "",
                "required": true,
                "valueType": "string",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }],
            "outputs": [{
                "key": "isEmpty",
                "label": "core.module.output.label.Search result empty",
                "type": "source",
                "valueType": "boolean",
                "targets": [{
                    "moduleId": "tc90wz",
                    "key": "switch"
                }]
            }, {
                "key": "unEmpty",
                "label": "core.module.output.label.Search result not empty",
                "type": "source",
                "valueType": "boolean",
                "targets": [{
                    "moduleId": "nlfwkc",
                    "key": "switch"
                }]
            }, {
                "key": "quoteQA",
                "label": "core.module.Dataset quote.label",
                "type": "source",
                "valueType": "datasetQuote",
                "targets": [{
                    "moduleId": "nlfwkc",
                    "key": "quoteQA"
                }]
            }, {
                "key": "finish",
                "label": "core.module.output.label.running done",
                "description": "core.module.output.description.running done",
                "valueType": "boolean",
                "type": "source",
                "targets": []
            }, {
                "key": "userChatInput",
                "label": "core.module.input.label.user question",
                "type": "hidden",
                "valueType": "string",
                "targets": [{
                    "moduleId": "nlfwkc",
                    "key": "userChatInput"
                }]
            }]
        }, {
            "moduleId": "q9equb",
            "name": "core.module.template.App system setting",
            "flowType": "userGuide",
            "position": {
                "x": -272.66416216517086,
                "y": 842.9928682053646
            },
            "inputs": [{
                "key": "welcomeText",
                "type": "hidden",
                "valueType": "string",
                "label": "core.app.Welcome Text",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "value": "你好，我是电影《星际穿越》 AI 助手，有什么可以帮助你的？\n[导演是谁]\n[剧情介绍]\n[票房分析]",
                "connected": false
            }, {
                "key": "variables",
                "type": "hidden",
                "valueType": "any",
                "label": "core.module.Variable",
                "value": [],
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "questionGuide",
                "valueType": "boolean",
                "type": "switch",
                "label": "",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }, {
                "key": "tts",
                "type": "hidden",
                "valueType": "any",
                "label": "",
                "showTargetInApp": false,
                "showTargetInPlugin": false,
                "connected": false
            }],
            "outputs": []
        }, {
            "moduleId": "tc90wz",
            "name": "指定回复",
            "flowType": "answerNode",
            "position": {
                "x": 1964.026271678838,
                "y": 663.4812247423405
            },
            "inputs": [{
                "key": "switch",
                "type": "target",
                "label": "core.module.input.label.switch",
                "description": "core.module.input.description.Trigger",
                "valueType": "any",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "connected": true
            }, {
                "key": "text",
                "type": "textarea",
                "valueType": "any",
                "label": "core.module.input.label.Response content",
                "description": "core.module.input.description.Response content",
                "placeholder": "core.module.input.description.Response content",
                "showTargetInApp": true,
                "showTargetInPlugin": true,
                "value": "对不起，我找不到你的问题，请更加详细的描述你的问题。",
                "connected": false
            }],
            "outputs": [{
                "key": "finish",
                "label": "core.module.output.label.running done",
                "description": "core.module.output.description.running done",
                "valueType": "boolean",
                "type": "source",
                "targets": []
            }]
        }]
    }
