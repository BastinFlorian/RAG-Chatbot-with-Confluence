# Demo
if __name__ == '__main__':
    from help_desk import HelpDesk

    model = HelpDesk(new_db=True)

    print(model.db._collection.count())

    prompt = 'Comment faire ma photo de profil Octo ?'
    result, sources = model.retrieval_qa_inference(prompt)
    print(result, sources)
