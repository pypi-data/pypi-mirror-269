import json
from importlib import reload
from unittest import mock

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms.renderers import DjangoTemplates
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

import galleryfield
from galleryfield import conf, defaults
from galleryfield.fields import GalleryFormField
from galleryfield.utils import get_formatted_thumbnail_size
from galleryfield.widgets import GalleryWidget
from tests import factories
from tests.test_fields import DemoTestGalleryModelForm


class GalleryWidgetTestMixin:
    @staticmethod
    def _get_rendered_field_html(field, print_output=False):
        class Form(forms.Form):
            f = field

        haystack = str(Form()['f'])
        if print_output:
            print(haystack)
        return haystack

    def assertFieldRendersIn(self, field, needle, strict=False, print_output=False):
        haystack = self._get_rendered_field_html(field, print_output)
        assert_in = self.assertInHTML if not strict else self.assertIn
        assert_in(needle, haystack)

    def assertFieldRendersNotIn(self, field, needle, print_output=False):
        haystack = self._get_rendered_field_html(field, print_output)
        self.assertNotIn(needle, haystack)

    def _render_widget(self, widget, name, value=None, attrs=None, **kwargs):
        django_renderer = DjangoTemplates()
        print_output = kwargs.pop("print_output", False)
        output = widget.render(name, value, attrs=attrs,
                               renderer=django_renderer, **kwargs)
        if print_output:
            print(output)
        return output

    def check_in_html(self, widget, name, value, html, attrs=None,
                      strict=False, print_output=False, **kwargs):
        output = self._render_widget(widget, name, value, attrs=attrs, **kwargs)
        assert_in = self.assertIn if strict else self.assertInHTML

        if print_output:
            print(output)

        if isinstance(html, str):
            html = [html]
        for _html in html:
            assert_in(_html, output)

    def check_not_in_html(self, widget, name, value, html, attrs=None, **kwargs):
        output = self._render_widget(widget, name, value, attrs=attrs, **kwargs)
        if isinstance(html, str):
            html = [html]
        for _html in html:
            self.assertNotIn(_html, output)


class GalleryWidgetTest(GalleryWidgetTestMixin, SimpleTestCase):

    def test_widget(self):
        field = GalleryFormField()
        self.assertIsInstance(field.widget, GalleryWidget)

    def test_required_widget_render(self):
        f = GalleryFormField(required=True)

        self.assertFieldRendersIn(
            f, '<input type="hidden" name="f" value="null"'
               ' class="django-galleryfield-files-field '
               ' hiddeninput" required id="id_f">')

        f = GalleryFormField(required=False)
        self.assertFieldRendersIn(
            f, '<input type="hidden" name="f" value="null"'
               ' class="django-galleryfield-files-field '
               ' hiddeninput" id="id_f">')

    def test_gallery_widget_render_with_value(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)
        image_data = [1]
        value = json.dumps(image_data)
        expected_result = (
            '<input type="hidden" name="image" value="[1]"')
        self.check_in_html(
            f.widget, "image", value, strict=True,  html=[expected_result])

    def test_gallery_widget_jquery_upload_options_max_number_of_files_overridden(self):  # noqa
        from random import randint
        max_number_of_file_ui_options_value = randint(1, 10)
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        f.widget.jquery_file_upload_ui_options.update(
            {"maxNumberOfFiles": max_number_of_file_ui_options_value})

        setattr(f.widget, "max_number_of_images", None)
        self.check_not_in_html(f.widget, "image", '', html="maxNumberOfFiles")

        f.widget = GalleryWidget(
            jquery_file_upload_ui_options={
                "maxNumberOfFiles": max_number_of_file_ui_options_value})
        setattr(f.widget, "max_number_of_images", 0)
        self.check_not_in_html(f.widget, "image", '', html="maxNumberOfFiles")

        max_number_of_file = randint(1, 10)
        f.widget = GalleryWidget(
            jquery_file_upload_ui_options={"maxNumberOfFiles": 0})

        setattr(f.widget, "max_number_of_images", max_number_of_file)
        expected_string = "maxNumberOfFiles: %i" % max_number_of_file
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)

    def test_gallery_widget_thumbnail_size(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)
        f.widget = GalleryWidget()
        expected_value = get_formatted_thumbnail_size(
                conf.DEFAULT_THUMBNAIL_SIZE).split("x")[0]
        expected_string = f"previewMaxWidth: {expected_value}"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)

        f.widget = GalleryWidget(thumbnail_size=130)
        expected_string = "previewMaxWidth: 130"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)
        expected_string = "previewMaxHeight: 130"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)

        f.widget = GalleryWidget(thumbnail_size=(135, 250))
        expected_string = "previewMaxWidth: 135"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)
        expected_string = "previewMaxHeight: 250"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)

        f.widget = GalleryWidget(thumbnail_size="130x260")
        expected_string = "previewMaxWidth: 130"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)
        expected_string = "previewMaxHeight: 260"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)

    def test_set_thumbnail_size_after_gallery_widget_init(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        f.widget = GalleryWidget(thumbnail_size=130)
        f.widget.thumbnail_size = 250
        expected_string = "previewMaxWidth: 250"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)
        expected_string = "previewMaxHeight: 250"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)

        f.widget.thumbnail_size = "111x222"
        expected_string = "previewMaxWidth: 111"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)
        expected_string = "previewMaxHeight: 222"
        self.check_in_html(f.widget, "image", '', strict=True, html=expected_string)

    def test_gallery_widget_jquery_upload_options_None(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)
        self.check_in_html(
            f.widget, "image", '', strict=True, html="disableImageResize")

        f.widget = GalleryWidget(
            jquery_file_upload_ui_options={"disableImageResize": None})
        self.check_not_in_html(f.widget, "image", '', html="disableImageResize")

    def test_gallery_widget_disabled(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)
        f.widget = GalleryWidget()
        file_upload_button = (
            '<input type="file" class="gallery-widget-image-input" '
            'id="%(field_name)s-files" multiple accept="image/*" '
            'data-action="%(upload_url)s">'
            % {"field_name": "image",
               "upload_url":
                   reverse(defaults.DEFAULT_UPLOAD_URL_NAME)}
        )
        self.check_in_html(
            f.widget, "image", '',
            html=[file_upload_button])

        f.widget.attrs["readonly"] = True
        self.check_not_in_html(
            f.widget, "image", '',
            # The css class of file input button
            html=["gallery-widget-image-input"])

    def test_gallery_widget_upload_handler_url_none(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)
        f.widget = GalleryWidget()
        file_upload_button = (
            '<input type="file" class="gallery-widget-image-input" '
            'id="%(field_name)s-files" multiple accept="image/*" '
            'data-action="%(upload_url)s">'
            % {"field_name": "image",
               "upload_url":
                   reverse(defaults.DEFAULT_UPLOAD_URL_NAME)}
        )
        self.check_in_html(
            f.widget, "image", '',
            html=[file_upload_button])

        f.widget.upload_url = None
        self.check_not_in_html(
            f.widget, "image", '',
            # The css class of file input button
            html=["gallery-widget-image-input"])

    def test_disabled_widget_render(self):
        f = GalleryFormField()
        self.assertFieldRendersIn(
            f, 'gallery-widget-image-input', strict=True, print_output=True)

        f = GalleryFormField(disabled=True)
        self.assertFieldRendersNotIn(f, 'gallery-widget-image-input')

    def test_widget_render_conflict(self):
        # the target image model is not the default,
        # some of the urls are default urls
        field = GalleryFormField(target_model="tests.FakeValidImageModel")

        test_case = {
            "galleryfield-builtingalleryimage-upload":
                {"upload_url": "test_image_upload"},
            "galleryfield-builtingalleryimage-crop":
                {"crop_request_url": "test_image_crop"},
            "galleryfield-builtingalleryimage-fetch":
                {"fetch_url": "test_images_fetch"}
        }

        default_urls = {
            "upload_url": "galleryfield-builtingalleryimage-upload",
            "crop_request_url": "galleryfield-builtingalleryimage-crop",
            "fetch_url": "galleryfield-builtingalleryimage-fetch"
        }

        for default, kwargs in test_case.items():
            with self.subTest(default=default, url_kwargs=kwargs):
                test_kwargs = default_urls.copy()
                test_kwargs.update(kwargs)

                field.widget = GalleryWidget(**test_kwargs)
                with self.assertRaises(ImproperlyConfigured) as cm:
                    self._render_widget(field.widget, "field", "")

                self.assertIn(
                    'You need to write your own views for your image model',
                    cm.exception.args[0], cm.exception)
                self.assertNotIn(
                    default,
                    cm.exception.args[0]
                )

    def test_widget_disable_fetch_no_conflict(self):
        field = GalleryFormField(target_model="tests.FakeValidImageModel")

        kwargs = {
            "upload_url": "test_image_upload",
            "fetch_url": "test_images_fetch",
            "disable_server_side_crop": True
        }

        field.widget = GalleryWidget(**kwargs)
        self._render_widget(field.widget, "field", "")

    def test_widget_disable_server_side_crop_no_conflict(self):
        field = GalleryFormField(target_model="tests.FakeValidImageModel")

        kwargs = {
            "upload_url": "test_image_upload",
            "fetch_url": "builtingalleryimage-fetch",  # a conflict URL
            "disable_fetch": True
        }

        field.widget = GalleryWidget(**kwargs)
        self._render_widget(field.widget, "field", "")

    def test_widget_no_conflict(self):
        # the target image model and all urls are not using the default,
        field = GalleryFormField(target_model="tests.FakeValidImageModel")

        kwargs = {
            "upload_url": "test_image_upload",
            "crop_request_url": "test_image_crop",
            "fetch_url": "test_images_fetch"
        }

        field.widget = GalleryWidget(**kwargs)
        # No error thrown
        self._render_widget(field.widget, "field", "")

    def test_widget_invalid_url(self):
        # the target image model and all urls are not using the default,
        field = GalleryFormField(target_model="tests.FakeValidImageModel")

        kwargs = {
            "upload_url": "test_image_upload",
            "fetch_url": "test_images_fetch"
        }

        invalid_url_name = "invalid-url-name"

        for k, v in kwargs.items():
            with self.subTest(key=k, value=v):
                test_kwargs = kwargs.copy()
                test_kwargs.update({k: invalid_url_name})

                field.widget = GalleryWidget(**test_kwargs)
                with self.assertRaises(ImproperlyConfigured) as cm:
                    self._render_widget(field.widget, "field", "")

                expected_error_str = "is not a valid view function or pattern name"

                self.assertIn(
                    expected_error_str,
                    str(cm.exception))

    def test_widget_set_jquery_file_upload_ui_options_None_get_default(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        f.widget.jquery_file_upload_ui_options = None
        self.assertDictEqual(
            f.widget.jquery_file_upload_ui_options,
            defaults.JQUERY_FILE_UPLOAD_UI_DEFAULT_OPTIONS)

    def test_widget_set_jquery_file_upload_ui_options_not_dict(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        with self.assertRaises(ImproperlyConfigured) as cm:
            f.widget.jquery_file_upload_ui_options = "foo-bar"

        expected_error_msg = "'jquery_file_upload_ui_options' must be a dict"
        self.assertIn(expected_error_msg, cm.exception.args[0])

    @mock.patch("django.forms.renderers.DjangoTemplates.render")
    def test_widget_set_jquery_file_upload_ui_options_render(self, mock_render):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        f.widget.jquery_file_upload_ui_options = {
            "autoUpload": True
        }
        self._render_widget(f.widget, "image")

        expected_string = "autoUpload: true"
        self.assertIn(
            expected_string,
            str(mock_render.call_args),
        )

    @mock.patch('galleryfield.widgets.logger.warning')
    @mock.patch("django.forms.renderers.DjangoTemplates.render")
    def test_widget_set_jquery_file_upload_ui_options_configured_maxNumberOfFiles(
            self, mock_render, mock_log):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        f.widget.jquery_file_upload_ui_options = {
            "maxNumberOfFiles": 10
        }

        expected_message = ("'maxNumberOfFiles' in 'jquery_file_upload_ui_options' "
                            "will be overridden later by the formfield")
        self.assertEqual(mock_log.call_count, 1)
        self.assertIn(expected_message, str(mock_log.call_args))
        self._render_widget(f.widget, "image")
        self.assertNotIn(
            "maxNumberOfFiles",
            str(mock_render.call_args.kwargs),
        )

    @mock.patch('galleryfield.widgets.logger.warning')
    @mock.patch("django.forms.renderers.DjangoTemplates.render")
    def test_widget_set_jquery_file_upload_ui_options_configured_preview_size(  # noqa
            self, mock_render, mock_log):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        values = [False, "false", "False"]

        for value in values:
            with self.subTest(value=value):

                f.widget.jquery_file_upload_ui_options = {
                    "singleFileUploads": value
                }

                expected_message = ("'singleFileUploads=False' in "
                                    "'jquery_file_upload_ui_options' is not "
                                    "allowed and will be ignored.")

                # self.assertEqual(mock_log.call_count, 1, list(mock_log.call_args))
                self.assertIn(expected_message, str(mock_log.call_args))
                self._render_widget(f.widget, "image")
                self.assertNotIn(
                    "singleFileUploads",
                    str(mock_render.call_args),
                )
                mock_render.reset_mock()
                mock_log.reset_mock()

    @mock.patch('galleryfield.widgets.logger.warning')
    @mock.patch("django.forms.renderers.DjangoTemplates.render")
    def test_widget_set_jquery_file_upload_ui_options_configured_singleFileUploads_true(  # noqa
            self, mock_render, mock_log):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)
        f.widget.thumbnail_size = "120x180"

        values = [{"previewMaxWidth": 100},
                  {"previewMaxHeight": 150}]

        expected_rendered_values = [
            "previewMaxWidth: 120",
            "previewMaxHeight: 180"]

        for i, value in enumerate(values):
            with self.subTest(value=value):

                f.widget.jquery_file_upload_ui_options = value

                expected_message = (
                    "'previewMaxWidth' and 'previewMaxHeight' "
                    "in 'jquery_file_upload_ui_options' are ignored.")
                # self.assertEqual(mock_log.call_count, 1)
                self.assertIn(expected_message, str(mock_log.call_args))
                self._render_widget(f.widget, "image")
                self.assertIn(
                    expected_rendered_values[i],
                    str(mock_render.call_args),
                )
                mock_render.reset_mock()
                mock_log.reset_mock()

    def test_widget_set_jquery_file_upload_ui_sortable_options_None_get_default(self):  # noqa
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        f.widget.jquery_file_upload_ui_sortable_options = None
        self.assertDictEqual(
            f.widget.jquery_file_upload_ui_sortable_options,
            defaults.JQUERY_FILE_UPLOAD_UI_DEFAULT_SORTABLE_OPTIONS)

    def test_widget_set_jquery_file_upload_ui_sortable_options_not_dict(self):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        with self.assertRaises(ImproperlyConfigured) as cm:
            f.widget.jquery_file_upload_ui_sortable_options = "foo-bar"

        expected_error_msg = (
            "'jquery_file_upload_ui_sortable_options' must be a dict")
        self.assertIn(expected_error_msg, cm.exception.args[0])

    @mock.patch("django.forms.renderers.DjangoTemplates.render")
    def test_widget_set_jquery_file_upload_ui_sortable_options_render(
            self, mock_render):
        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)

        f.widget.jquery_file_upload_ui_sortable_options = {
            "delay": 400
        }
        self._render_widget(f.widget, "image")

        expected_string = "delay: 400"
        self.assertIn(
            expected_string,
            str(mock_render.call_args),
        )

        self.assertIn(
            "disabled: false",
            str(mock_render.call_args),
        )


class GalleryWidgetConfTest(GalleryWidgetTestMixin, SimpleTestCase):
    @staticmethod
    def reload_defaults_and_conf():
        reload(galleryfield.defaults)
        reload(galleryfield.conf)

    @override_settings(DJANGO_GALLERY_FIELD_CONFIG={"bootstrap_version": 5})
    @mock.patch("django.forms.renderers.DjangoTemplates.render")
    def test_widget_bootstrap_version_render(self, mock_render):
        self.reload_defaults_and_conf()

        f = GalleryFormField(target_model=defaults.DEFAULT_TARGET_IMAGE_MODEL)
        self._render_widget(f.widget, "image")
        expected_string = "showElementClass: 'show'"
        self.assertIn(
            expected_string,
            str(mock_render.call_args),
        )

    def test_conf_static_with_different_bootstrap_versions(self):
        for bootstrap_version in [3, 4, 5]:
            with override_settings(
                    DJANGO_GALLERY_FIELD_CONFIG={
                        "bootstrap_version": bootstrap_version}):
                self.reload_defaults_and_conf()

                self.assertEqual(
                    conf.BOOTSTRAP_CSS_LOCATION,
                    defaults.DEFAULT_STATICS["bootstrap_css"][bootstrap_version])

                self.assertEqual(
                    conf.BOOTSTRAP_JS_LOCATION,
                    defaults.DEFAULT_STATICS["bootstrap_js"][bootstrap_version])


class GalleryWidgetTestExtra(TestCase):
    # This test cases need db support
    def setUp(self) -> None:
        factories.UserFactory.reset_sequence()
        factories.BuiltInGalleryImageFactory.reset_sequence()
        factories.DemoGalleryFactory.reset_sequence()
        self.user = factories.UserFactory()
        super().setUp()

    def test_no_fetch_url(self):
        gallery_obj = factories.DemoGalleryFactory.create(
            creator=self.user, number_of_images=5, shuffle=True)
        pks = list(gallery_obj.images)

        form = DemoTestGalleryModelForm(instance=gallery_obj)

        rendered_js_content = "// fetching existing images"
        rendered_js_instance_data = f"({pks})"
        self.assertIn(rendered_js_content, form.as_table())
        self.assertIn(rendered_js_instance_data, form.as_table())

        # now we set fetch_url=None to the widget
        form.fields["images"].widget.fetch_url = None

        self.assertNotIn(rendered_js_content, form.as_table())
        self.assertNotIn(rendered_js_instance_data, form.as_table())

    def test_no_crop_disabled(self):
        gallery_obj = factories.DemoGalleryFactory.create(
            creator=self.user, number_of_images=5, shuffle=True)

        form = DemoTestGalleryModelForm(instance=gallery_obj)

        # This data attribute only exists in Edit buttons
        rendered_button_data_toggle = 'data-toggle="modal"'
        self.assertIn(rendered_button_data_toggle, form.as_table())

        # # now we set crop_request_url=None to the widget
        form.fields["images"].widget.disable_server_side_crop = True
        self.assertNotIn(rendered_button_data_toggle, form.as_table())
