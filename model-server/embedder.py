from sentence_transformers import SentenceTransformer, models
from ko_sentence_transformers.models import KoBertTransformer

class Embedder():
    # static
    # 글자 평균 길이 274, 최대 길이 5728
    word_embedding_model = KoBertTransformer("monologg/kobert", max_seq_length=512) 
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode='mean')
    embedder = SentenceTransformer(modules=[word_embedding_model, pooling_model])