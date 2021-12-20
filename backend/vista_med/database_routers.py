class VistaMedRouter:
    """
    A router to forbid all migrations on the database with alias "vista-med"
    """

    vista_med_app_label = "vista_med"
    vista_med_db_alias = "vista-med"

    def db_for_read(self, model, **hints):
        """
        Route reading of vista_med app models
        to the database with alias "vista-med"
        """
        if model._meta.app_label == self.vista_med_app_label:
            return self.vista_med_db_alias
        return None

    def db_for_write(self, model, **hints):
        """
        Raise RuntimeError when trying to write vista_med models.
        """
        if model._meta.app_label == self.vista_med_app_label:
            raise RuntimeError(f"models of {self.vista_med_app_label} app are read-only")
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure no migrations are performed
        on the database with alias "vista-med"
        """
        if db == self.vista_med_db_alias:
            return False
        return None
