from ask import get_collection, retrieve

tests = [
    ("relevant", "What does the p-value mean?", "hypothesis_testing.md"),
    ("relevant", "What is overfitting?", "machine_learning_basics.md"),
    ("relevant", "Which activation function is used for multi-class output?", "neural_networks.md"),
    ("relevant", "What does git push do?", "git_workflow.md"),
    ("relevant", "What is a foreign key?", "databases_sql.md"),
    ("relevant", "How do I stop Git from tracking secret files?", "git_workflow.md"),
    ("irrelevant", "What is the capital of Australia?", None),
    ("irrelevant", "How do I bake a chocolate cake?", None),
    ("irrelevant", "What is the Wi-Fi password in the lab?", None),
    ("irrelevant", "What is Kubernetes?", None),
    ("irrelevant", "How do I train a random forest?", None),
]

collection = get_collection()
for kind, question, expected in tests:
    best = retrieve(collection, question, k=1)[0]
    check = "" if expected is None else ("OK" if best["source"] == expected else "WRONG")
    print(f"{best['distance']:.3f}  {kind:10}  {check:5}  {question}  ->  {best['source']}")