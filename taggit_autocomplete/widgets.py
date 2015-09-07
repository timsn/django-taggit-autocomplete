from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from taggit.models import Tag

from utils import edit_string_for_tags


class TagAutocomplete(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
        html = super(TagAutocomplete, self).render(name, value, attrs)
        tags = Tag.objects.values_list('name', flat=True)

        tagsJson = "[" + ",".join('"{0}"'.format(tag) for tag in tags) + "]"
        js = u'''<script type="text/javascript">
        var availableTags = %s;
            function split( val ) {
              return val.split( /,\\s*/ );
            }
            function extractLast( term ) {
              return split( term ).pop();
            }
        jQuery().ready(function() {
            jQuery("#%s")
              // don't navigate away from the field on tab when selecting an item
              .bind( "keydown", function( event ) {
                if ( event.keyCode === $.ui.keyCode.TAB &&
                    $( this ).autocomplete( "instance" ).menu.active ) {
                  event.preventDefault();
                }
              })
              .autocomplete({
                minLength: 0,
                source: function( request, response ) {
                  // delegate back to autocomplete, but extract the last term
                  response( $.ui.autocomplete.filter(
                    availableTags, extractLast( request.term ) ) );
                },
                focus: function() {
                  // prevent value inserted on focus
                  return false;
                },
                select: function( event, ui ) {
                  var terms = split( this.value );
                  // remove the current input
                  terms.pop();
                  // add the selected item
                  terms.push( ui.item.value );
                  // add placeholder to get the comma-and-space at the end
                  terms.push( "" );
                  this.value = terms.join( ", " );
                  return false;
                }
            });
        }); </script>''' % (tagsJson, attrs['id'])
        return mark_safe("\n".join([html, js]))

    class Media:
        js_base_url = getattr(settings, 'TAGGIT_AUTOCOMPLETE_JS_BASE_URL','%s/jquery' % settings.MEDIA_URL)
        css = {
            'all': ('%s/jquery-ui.min.css' % js_base_url,)
        }
        js = (
            '%s/jquery.min.js' % js_base_url,
            '%s/jquery-ui.min.js' % js_base_url,
            )
