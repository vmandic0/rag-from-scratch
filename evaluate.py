from ask import NO_ANSWER, answer, get_collection, retrieve
from config import CHUNK_OVERLAP, CHUNK_WORDS, MAX_DISTANCE, TOP_K


TESTS = [
    ("Which status code means a resource was created?", "web_http_rest.md", "201"),
    ("What is the default port for HTTPS?", "web_http_rest.md", "443"),
    ("How do I send a token to the server for authentication?", "web_http_rest.md", "Bearer"),
    ("Why is the sample variance divided by n minus 1?", "statistics_basics.md", "Bessel"),
    ("What share of values lies within two standard deviations in a normal distribution?", "statistics_basics.md", "95"),
    ("What significance level is usually used to reject the null hypothesis?", "hypothesis_testing.md", "0.05"),
    ("Which test checks the relationship between two categorical variables?", "hypothesis_testing.md", "chi-square"),
    ("What is a common split of data into training, validation and test sets?", "machine_learning_basics.md", "70"),
    ("Which activation function is the default for hidden layers?", "neural_networks.md", "ReLU"),
    ("How do I create and switch to a new branch?", "git_workflow.md", "checkout -b"),
    ("Which join keeps all rows from the left table?", "databases_sql.md", "LEFT JOIN"),
    ("What do the letters ACID stand for in transactions?", "databases_sql.md", "atomicity"),
    ("What is the capital of Australia?", None, None),
    ("What is Kubernetes?", None, None),
    ("How do I train a random forest?", None, None),
    ("Who won the football World Cup in 2018?", None, None),
]


if __name__ == "__main__":
    collection = get_collection()
    top1_total = 0
    topk_total = 0
    keyword_total = 0
    refusal_total = 0

    for question, expected_source, keyword in TESTS:
        hits = retrieve(collection, question, k=TOP_K)
        result = answer(collection, question)
        distance = hits[0]["distance"]

        if expected_source is None:
            refusal_ok = result["answer"] == NO_ANSWER
            refusal_total += refusal_ok
            marks = f"refusal={'OK' if refusal_ok else 'FAIL'}"
        else:
            top1_ok = hits[0]["source"] == expected_source
            topk_ok = expected_source in {hit["source"] for hit in hits}
            keyword_ok = keyword.lower() in result["answer"].lower()
            top1_total += top1_ok
            topk_total += topk_ok
            keyword_total += keyword_ok
            marks = (
                f"top1={'OK' if top1_ok else 'FAIL'} "
                f"topk={'OK' if topk_ok else 'FAIL'} "
                f"keyword={'OK' if keyword_ok else 'FAIL'}"
            )

        print(f"{marks} | {question} | distance={distance:.3f}")
        if expected_source is not None:
            print(f"  {result['answer']}")

    print(f"top-1 retrieval: {top1_total}/12")
    print(f"top-k retrieval: {topk_total}/12")
    print(f"keyword in answer: {keyword_total}/12")
    print(f"correct refusals: {refusal_total}/4")
    print(f"CHUNK_WORDS: {CHUNK_WORDS}")
    print(f"CHUNK_OVERLAP: {CHUNK_OVERLAP}")
    print(f"TOP_K: {TOP_K}")
    print(f"MAX_DISTANCE: {MAX_DISTANCE}")
