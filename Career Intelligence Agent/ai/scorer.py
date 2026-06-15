from sklearn.metrics.pairwise import cosine_similarity

def score(cv_emb, job_emb):

    return cosine_similarity(
        [cv_emb],
        [job_emb]
    )[0][0]