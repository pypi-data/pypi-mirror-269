def get_favorited_list(user, model,class_name):
    """
    Get favorited items for a given user and model (Store or Restaurant).
    """
    return class_name.objects.filter(user=user, favourited=True, **{f'{model}__isnull': False})