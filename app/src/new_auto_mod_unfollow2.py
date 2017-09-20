#!venv/bin/python
# -*- coding: utf-8 -*-
from app.src.new_unfollow import new_unfollow


def new_auto_mod_unfollow2(self):
    log_string = "Trying to unfollow: %s" % (self.current_user)
    self.write_log(log_string)
    new_unfollow(self, self.current_id, self.current_user)
