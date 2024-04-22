def save_data_to_db(model_instance, *args):
    db_instance = model_instance()
    # db_instance.save()
    fields = args[0]
    values = args[1]
    for field, value in zip(fields, values):
        setattr(db_instance, field, value)
    db_instance.save()
    