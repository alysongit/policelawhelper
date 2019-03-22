import xadmin
from xadmin.views.detail import ResultField
from cms.models import Article, Tab, CoverPicture
from apps.admin import BaseAdmin


class ArticelAdmin(BaseAdmin):
    model_icon = 'fa fa-book'

    list_display = ["title", "tab_name", "sort", "law_extract", "source", "last_update_user_name",
                    "format_cover_pics", "cover_pics_view"]
    list_display_links = ["title"]
    list_editable = ["title", "law_extract", "sort"]
    list_filter = ["law_extract", "tab"]
    search_fields = ["title"]
    show_detail_fields = ["title"]

    def tab_name(self, obj):
        tab = obj.tab
        tab_name = ""
        if tab:
            tab_name = tab.name
        html = '<div><a href="/admin/cms/tab/?_p_id__contains={}" target="_blank">{}</a></div>'.\
        format(tab.id, tab_name)
        return html
    tab_name.short_description = "栏目名称"
    tab_name.allow_tags = True

    show_bookmarks = True
    list_bookmarks = []

    list_export = ["xls", "xml", "json"]
    list_export_fields= ["title"]

    fields = ["tab", "title", "source", "law_extract", "sort", "cover_pics", "content"]

    def get_field_result(self, field_name):
        if field_name == "content":
            field_name = "format_content"
        if field_name == "cover_pics":
            field_name = "format_cover_pics"
        return ResultField(self.obj, field_name, self)

    def format_content(self, obj):
        content = format(obj.content)
        return content
    format_content.short_descriotion = "内容"
    format_content.allow_tags = True

    def format_cover_pics(self, obj):
        cover_pics = obj.cover_pics.all().order_by("sort")
        html = ""
        for pic in cover_pics:
            try:
                html += '<img src="{}" width="100px">'.format(pic.image.url)
            except:
                pass
        format(html)
        return html
    format_cover_pics.short_description = "封面图"
    format_cover_pics.allow_tags = True

    def cover_pics_view(self, obj):
        html = '<span>' \
               '<a href="{}" target="_blank">查看</a>' \
               '</span>'.format(
            "/admin/cms/coverpicture/?article_id={}".format(obj.id),
        )
        format(html)
        return html
    cover_pics_view.short_description = "查看封面图"
    cover_pics_view.allow_tags = True


class TabAdmin(BaseAdmin):
    model_icon = 'fa fa-sitemap'

    list_display = ["id", "detail_name", "parent_name", "fixed", "sort", "tab_type",
                    "last_update_user_name", "last_update_time", "article_view"]
    list_editable = ["sort", "fixed", "tab_type"]
    search_fields = ["name"]
    list_filter = ["fixed", "id"]
    show_detail_fields = ["detail_name"]
    ordering = ["sort"]

    show_bookmarks = True
    list_bookmarks = []

    list_export = ["xls", "xml", "json"]
    list_export_fields = ["name"]

    fields = ["name", "parent", "fixed", "sort", "tab_type"]

    def queryset(self):
        qs = super(TabAdmin, self).queryset()
        if self.request.get_full_path().find("?") != -1:
            return qs
        else:
            qs = qs.filter(level=0)
            return qs

    def article_view(self, obj):
        html = '<div style="text-align: center;">' \
               '<button style="margin-top:5px;margin-right:10px;">' \
               '<a href="/admin/cms/article/add/?tab={}" target="_blank">{}</a>' \
               '</button>' \
               '<button style="margin-top:5px;">' \
               '<a href="/admin/cms/article/?_p_tab__id__exact={}" target="_blank">{}</a>' \
               '</button>' \
               '</div>'.format(
            obj.id,
            "新建内容",
            obj.id,
            "查看内容({}个内容)".format(Article.objects.filter(tab_id=obj.id).count())
        )
        format(html)
        return html
    article_view.short_description = "内容"
    article_view.allow_tags = True

    def detail_name(self, obj):
        if obj.parent:
            name = "{}>{}".format(obj.parent.name, obj.name)
        else:
            name = obj.name
        children = obj.get_children()
        if children:
            html = '<span>' \
                   '<a href="{}" target="_blank">{}({}个子栏目)</a>' \
                   '</span>'.format(
                "/admin/cms/tab/?_rel_parent__id__exact={}".format(obj.id),
                name,
                len(children),
            )
            format(html)
        else:
            html = name
        return html
    detail_name.short_description = "栏目名称"
    detail_name.allow_tags = True

    def parent_name(self, obj):
        if obj.parent:
            html = '<span>' \
                   '<a href="{}" target="_blank">{}</a>' \
                   '</span>'.format(
                "/admin/cms/tab/?_p_id__contains={}".format(obj.parent.id),
                obj.parent.name,
            )
            format(html)
        else:
            html = ""
        return html
    parent_name.short_description = "父栏目"
    parent_name.allow_tags = True


class CoverPictureAdmin(BaseAdmin):
    model_icon = 'fa fa-folder'

    list_display = ["name", "format_image", "sort"]
    list_editable = ["name", "sort"]
    list_display_links = ["name"]
    list_filter = ["id"]
    search_fields = ["id"]
    fields = ["name", "image", "sort"]

    def format_image(self, obj):
        html = ""
        html += '<img src="{}" width="100px">'.format(obj.image.url)
        format(html)
        return html
    format_image.short_description = "图片"
    format_image.allow_tags = True

    def queryset(self):
        article_id = self.request.GET.get("article_id")
        if article_id:
            qs = CoverPicture.objects.filter(article=article_id).all().order_by("-sort")
            return qs
        else:
            qs = super(CoverPictureAdmin, self).queryset()
            return qs

xadmin.site.register(Tab, TabAdmin)
xadmin.site.register(Article, ArticelAdmin)
xadmin.site.register(CoverPicture, CoverPictureAdmin)