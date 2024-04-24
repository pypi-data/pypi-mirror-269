# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Base Django settings for Lino Noi applications.

"""

from lino.projects.std.settings import *
from lino_noi import SETUP_INFO
from lino.api import _


class Site(Site):

    verbose_name = "Lino Noi"
    description = SETUP_INFO['description']
    version = SETUP_INFO['version']
    url = SETUP_INFO['url']
    quantity_max_length = 7
    # project_model = 'tickets.Site'
    # 20221214 : in noi we don't want Order to point to Site.

    demo_fixtures = [
        'std', 'minimal_ledger', 'demo', 'demo2', 'demo_bookings',
        'checksummaries', 'checkdata'
    ]  # 'linotickets', 'tractickets', 'luc']

    # project_model = 'tickets.Project'
    # project_model = 'deploy.Milestone'
    textfield_format = 'html'
    user_types_module = 'lino_noi.lib.noi.user_types'
    workflows_module = 'lino_noi.lib.noi.workflows'
    custom_layouts_module = 'lino_noi.lib.noi.layouts'
    obj2text_template = "**{0}**"

    default_build_method = 'appyodt'

    # experimental use of rest_framework:
    # root_urlconf = 'lino_book.projects.noi1e.urls'

    # TODO: move migrator to lino_noi.projects.team
    migration_class = 'lino_noi.lib.noi.migrate.Migrator'

    auto_configure_logger_names = "lino lino_xl lino_noi"

    def get_installed_plugins(self):
        """Implements :meth:`lino.core.site.Site.get_installed_plugins` for Lino
        Noi.

        """
        yield super().get_installed_plugins()
        # yield 'lino.modlib.extjs'
        # yield 'lino.modlib.bootstrap3'
        yield 'lino.modlib.gfks'
        yield 'lino.modlib.help'
        # yield 'lino.modlib.system'
        # yield 'lino.modlib.users'
        yield 'lino_noi.lib.contacts'
        yield 'lino_noi.lib.users'
        yield 'lino_noi.lib.cal'
        yield 'lino_xl.lib.calview'
        # yield 'lino_xl.lib.extensible'
        # yield 'lino_noi.lib.courses'
        # yield 'lino_noi.lib.products'

        yield 'lino_xl.lib.topics'
        # yield 'lino_xl.lib.votes'
        # yield 'lino_xl.lib.stars'
        yield 'lino_noi.lib.tickets'
        yield 'lino_xl.lib.nicknames'
        # yield 'lino_xl.lib.skills'
        # yield 'lino_xl.lib.deploy'
        yield 'lino_xl.lib.working'
        yield 'lino_xl.lib.lists'
        # yield 'lino_xl.lib.blogs'

        yield 'lino.modlib.changes'
        yield 'lino.modlib.notify'
        yield 'lino.modlib.uploads'
        # yield 'lino_xl.lib.outbox'
        # yield 'lino_xl.lib.excerpts'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.smtpd'
        yield 'lino.modlib.weasyprint'
        yield 'lino_xl.lib.appypod'
        yield 'lino.modlib.checkdata'
        # yield 'lino.modlib.wkhtmltopdf'
        yield 'lino.modlib.dashboard'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi.lib.noi'
        # yield 'lino_xl.lib.inbox'
        # yield 'lino_xl.lib.mailbox'
        # yield 'lino_xl.lib.meetings'
        # yield 'lino_xl.lib.github'
        # yield 'lino.modlib.social_auth'
        yield 'lino_xl.lib.userstats'
        yield 'lino_noi.lib.groups'
        # yield 'lino_noi.lib.groups'

        yield 'lino_noi.lib.products'
        yield 'lino_noi.lib.trading'
        yield 'lino_xl.lib.storage'
        # yield 'lino_xl.lib.invoicing'  # no need to mention since subscriptions needs it
        yield 'lino_noi.lib.subscriptions'

        # if self.has_feature('cms_functionality'):
        yield 'lino_xl.lib.pages'
        # yield 'lino.modlib.publisher'

    def get_plugin_configs(self):
        yield super().get_plugin_configs()
        yield 'linod', 'use_channels', True
        # yield 'topics', 'hidden', True
        yield 'topics', 'partner_model', 'users.User'
        yield 'help', 'make_help_pages', True
        yield 'tickets', 'end_user_model', 'contacts.Person'
        yield 'working', 'ticket_model', 'tickets.Ticket'
        # yield ('system', 'use_dashboard_layouts', True)
        yield 'invoicing', 'order_model', 'subscriptions.Subscription'
        yield 'users', 'allow_online_registration', True
        yield 'summaries', 'duration_max_length', 10
        yield 'nicknames', 'named_model', 'tickets.Ticket'
        # yield 'pages', 'hidden', True

    def setup_actions(self):
        super().setup_actions()
        from lino.modlib.changes.utils import watch_changes as wc
        wc(self.modules.tickets.Ticket, ignore=['_user_cache'])
        wc(self.modules.comments.Comment, master_key='owner')
        # wc(self.modules.tickets.Link, master_key='ticket')
        # wc(self.modules.working.Session, master_key='owner')

        if self.is_installed('votes'):
            wc(self.modules.votes.Vote, master_key='votable')

        if self.is_installed('deploy'):
            wc(self.modules.deploy.Deployment, master_key='ticket')

        # if self.is_installed('extjs'):
        #     self.plugins.extjs.autorefresh_seconds = 0

        # from lino.core.merge import MergeAction
        # from lino_xl.lib.contacts.roles import ContactsStaff
        # lib = self.models
        # for m in (lib.contacts.Company, ):
        #     m.define_action(merge_row=MergeAction(
        #         m, required_roles=set([ContactsStaff])))


    # def setup_quicklinks(self, user, tb):
    #     super().setup_quicklinks(user, tb)
    #     # tb.add_action(self.models.courses.MyActivities)
    #     # tb.add_action(self.models.meetings.MyMeetings)
    #     # tb.add_action(self.modules.deploy.MyMilestones)
    #     # tb.add_action(self.models.tickets.MyTickets)
    #     # tb.add_action(self.models.tickets.TicketsToTriage)
    #     # tb.add_action(self.models.tickets.TicketsToTalk)
    #     # tb.add_action(self.modules.tickets.TicketsToDo)
    #     tb.add_action(self.models.tickets.RefTickets)
    #     tb.add_action(self.models.tickets.ActiveTickets)
    #     tb.add_action(self.models.tickets.AllTickets)
    #     tb.add_action(
    #         self.models.tickets.AllTickets.insert_action,
    #         label=_("Submit a ticket"))

    # def do_site_startup(self):
    #     super().do_site_startup()


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

USE_TZ = True
# TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = 'Europe/Tallinn'
TIME_ZONE = 'UTC'
