from pybackend_libs.dataelem.utils.lazy_loader import lazy

bge = lazy('pybackend_libs.dataelem.model.embedding.bge')
gte = lazy('pybackend_libs.dataelem.model.embedding.gte')
me5 = lazy('pybackend_libs.dataelem.model.embedding.me5')
jina = lazy('pybackend_libs.dataelem.model.embedding.jina')
baichuan = lazy('pybackend_libs.dataelem.model.llm.baichuan')
chatglm2 = lazy('pybackend_libs.dataelem.model.llm.chatglm2')
chatglm3 = lazy('pybackend_libs.dataelem.model.llm.chatglm3')
code_geex2 = lazy('pybackend_libs.dataelem.model.llm.code_geex2')
internlm = lazy('pybackend_libs.dataelem.model.llm.internlm')
llama2 = lazy('pybackend_libs.dataelem.model.llm.llama2')
qwen = lazy('pybackend_libs.dataelem.model.llm.qwen')
qwen1_5 = lazy('pybackend_libs.dataelem.model.llm.qwen1_5')
xverse = lazy('pybackend_libs.dataelem.model.llm.xverse')
visualglm = lazy('pybackend_libs.dataelem.model.mmu.visualglm')
vllm_model = lazy('pybackend_libs.dataelem.model.vllm.vllm_model')
layout_mrcnn = lazy('pybackend_libs.dataelem.model.layout.layout_mrcnn')
table_mrcnn = lazy('pybackend_libs.dataelem.model.table.table_mrcnn')
table_app = lazy('pybackend_libs.dataelem.model.table.table_app')
yi_base = lazy('pybackend_libs.dataelem.model.llm.yi')
lc_model = lazy('pybackend_libs.dataelem.model.llama_cpp.lc_model')
yuan_base = lazy('pybackend_libs.dataelem.model.llm.yuan')

latex_det = lazy('pybackend_libs.dataelem.model.ocr.latex_det')
latex_recog = lazy('pybackend_libs.dataelem.model.ocr.latex_recog')


def get_model(name: str):
    model_name_mapping = {
        'ChatGLM2': chatglm2,
        'ChatGLM3': chatglm3,
        'BaichuanChat': baichuan,
        'QwenChat': qwen,
        'Qwen1_5Chat': qwen1_5,
        'Llama2Chat': llama2,
        'VisualGLM': visualglm,
        'XverseChat': xverse,
        'InternLMChat': internlm,
        'ME5Embedding': me5,
        'BGEZhEmbedding': bge,
        'JINAEmbedding': jina,
        'GTEEmbedding': gte,
        'LayoutMrcnn': layout_mrcnn,
        'TableCellApp': table_app,
        'TableRowColApp': table_app,
        'MrcnnTableDetect': table_mrcnn,
        'VLLMModel': vllm_model,
        'YiBase': yi_base,
        'YuanBase': yuan_base,
        'LlamaCppModel': lc_model,
        'LatexDetection': latex_det,
        'LatexRecog': latex_recog
    }
    assert name in model_name_mapping, f'Unknown model name: {name}'
    return getattr(model_name_mapping[name], name)
