

import os

from kivy_garden.ebs.core.image import BleedImage
from kivy_garden.ebs.core.labels import ColorLabel

from kivy_garden.ebs.core.image import StandardImage
from kivy_garden.ebs.core.labels import SelfScalingLabel
from kivy_garden.ebs.core.colors import ColorBoxLayout

from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui


class ModularApiEngineManagerGuiMixin(BaseIoTNodeGui):
    def __init__(self, *args, **kwargs):
        super(ModularApiEngineManagerGuiMixin, self).__init__(*args, **kwargs)

        self._api_internet_link = None
        self._api_internet_link_indicator = None

        self._api_internet_connected = False
        self._api_internet_indicator = None

        self._api_connection_status = {}
        self._api_connection_indicators = {}

    @property
    def modapi_internet_link_indicator(self):
        if not self._api_internet_link_indicator:
            params = {'bgcolor': (0xff / 255., 0x00 / 255., 0x00 / 255., self.gui_tag_alpha),
                      'color': [1, 1, 1, 1]}
            self._api_internet_link_indicator = ColorLabel(
                text=self._api_internet_link, size_hint=(None, None),
                height=50, font_size='14sp',
                valign='middle', halign='center', **params
            )

            def _set_label_width(_, texture_size):
                self._api_internet_link_indicator.width = texture_size[0] + 20

            self._api_internet_link_indicator.bind(texture_size=_set_label_width)
        return self._api_internet_link_indicator

    def _modapi_internet_link_indicator_show(self, duration=5):
        _ = self.modapi_internet_link_indicator
        if not self._api_internet_link_indicator.parent:
            self.gui_notification_row.add_widget(self._api_internet_link_indicator)
            self.gui_notification_update()
        if duration:
            self.reactor.callLater(duration, self._modapi_internet_link_indicator_clear)

    def _modapi_internet_link_indicator_clear(self):
        if self._api_internet_link_indicator and self._api_internet_link_indicator.parent:
            self.gui_notification_row.remove_widget(self._api_internet_link_indicator)
            self.gui_notification_update()
        self._api_internet_link_indicator = None

    @property
    def modapi_internet_indicator(self):
        if not self._api_internet_indicator:
            _root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
            _source = os.path.join(_root, 'images', 'no-internet.png')
            self._api_internet_indicator = BleedImage(
                source=_source, pos_hint={'left': 1},
                size_hint=(None, None), height=50, width=50,
                bgcolor=(0xff / 255., 0x00 / 255., 0x00 / 255., self.gui_tag_alpha),
            )
        return self._api_internet_indicator

    def _modapi_internet_indicator_show(self):
        if not self.modapi_internet_indicator.parent:
            self.gui_notification_row.add_widget(self.modapi_internet_indicator)
            self.gui_notification_update()

    def _modapi_internet_indicator_clear(self):
        if self.modapi_internet_indicator.parent:
            self.modapi_internet_indicator.parent.remove_widget(self.modapi_internet_indicator)
            self.gui_notification_update()

    def modapi_connection_indicator(self, prefix):
        if prefix not in self._api_connection_indicators.keys():
            _root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
            source = os.path.join(_root, 'images', 'no-server.png')
            indicator = ColorBoxLayout(
                pos_hint={'left': 1}, orientation='horizontal',
                size_hint=(None, None), height=50, spacing=0,
                bgcolor=(0xff / 255., 0x00 / 255., 0x00 / 255., self.gui_tag_alpha),
            )
            indicator.add_widget(
                StandardImage(source=source, size_hint=(1, None), height=50)
            )
            indicator.add_widget(
                SelfScalingLabel(text=prefix)
            )

            self._api_connection_indicators[prefix] = indicator
        return self._api_connection_indicators[prefix]

    def _modapi_connection_indicator_show(self, prefix):
        if not self.modapi_connection_indicator(prefix).parent:
            self.gui_notification_row.add_widget(self.modapi_connection_indicator(prefix))
            self.gui_notification_update()

    def _modapi_connection_indicator_clear(self, prefix):
        if self.modapi_connection_indicator(prefix).parent:
            self.modapi_connection_indicator(prefix).parent.remove_widget(self.modapi_connection_indicator(prefix))
            self.gui_notification_update()

    def modapi_signal_internet_link(self, value, prefix):
        self._api_internet_link = value
        self._modapi_internet_link_indicator_show()

    def modapi_signal_internet_connected(self, value, prefix):
        if not value:
            self._modapi_internet_indicator_show()
        else:
            self._modapi_internet_indicator_clear()
        self._api_internet_connected = value

    def modapi_signal_api_connected(self, value, prefix):
        if not value:
            self._modapi_connection_indicator_show(prefix)
        else:
            self._modapi_connection_indicator_clear(prefix)
        self._api_connection_status[prefix] = value

    def modapi_signal_api_params_not_ready(self, error, prefix):
        self.log.warn(f"{prefix} : {error.msg}")

    def modapi_signal_api_server_not_ready(self, error, prefix):
        self.log.warn(f"{prefix} : {error.msg}")
