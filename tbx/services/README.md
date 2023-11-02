# NOTE

In commit e9a4558696f7e2ca1c6f9779ce11206d1e22d2ec, all references to the `tbx.services` app were removed. In addition, all models in `tbx.services.models.py` were removed.

There's nothing in the `tbx.services` app that is being used on the project. _Ideally_, `"tbx.services"` should be removed from [`INSTALLED_APPS`](https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-INSTALLED_APPS), and the `services` app directory deleted once the following migrations have been deployed:

- `0043_delete_service_pages.py`
- `0044_drop_all_tables.py`

However, doing so will break the project, with errors such as:

```console
django.db.migrations.exceptions.NodeNotFoundError: Migration torchbox.0133_remove_aboutpage_and_related_models dependencies reference nonexistent parent node ('services', '0029_subservice_listingsettings')

```

We could squash out references to the app in other apps’ migrations ... However, this is not a trivial task, as it requires a lot of manual work which would potentially introduce errors and result in data loss.

```console
Manual porting required
  Your migrations contained functions that must be manually copied over,
  as we could not safely copy their implementation.
  See the comment at the top of the squashed migration for details.
```

Therefore, it is probably safer to leave the app and the migrations in place.

---
