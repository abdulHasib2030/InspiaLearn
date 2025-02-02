import django_tables2 as tables
from learner.models import purchaseCourseModel

class CourseBuyersTable(tables.Table):
    # name =  tables.Column(orderable=True, verbose_name="Name")
    # title =  tables.Column(orderable=True, verbose_name="Course title")
    # price =  tables.Column(orderable=True, verbose_name="Price")
    # review =  tables.Column(orderable=False, verbose_name="Review	")
    # date =  tables.Column(orderable=False, verbose_name="Date")
    user = tables.Column(accessor="user.user.first_name", orderable=True, verbose_name="Name")
    class Meta:
        model = purchaseCourseModel
        template_name = "django_tables2/bootstrap4.html"
        fields = ("user", "course", "main_price", "discount", "percent", "date", "dateTime")
    def render_course(self, value):
        return ", ".join([course.landing_page.title for course in value.all()]) 
