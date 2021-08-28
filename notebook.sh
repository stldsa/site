ipython profile create
echo 'c.InteractiveShellApp.extensions = ["configurations"]' >> /root/.ipython/profile_default/ipython_config.py
python manage.py shell_plus --notebook