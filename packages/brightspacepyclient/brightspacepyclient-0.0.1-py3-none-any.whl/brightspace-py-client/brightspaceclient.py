from src.utils import RequestsSessionWrapper
from src.models.Response import ModuleResponse, AuthResponse


class BrightSpaceClient:
    _version: float
    _session: RequestsSessionWrapper

    def __init__(self, base_url: str, d2lsessionval: str, d2lsecuresessionval: str, xcsrftoken: str,
                 version: float) -> None:
        super().__init__()

        self._version = version

        self._session = RequestsSessionWrapper(base_url)
        self._session.headers.update({"x-csrf-token": xcsrftoken})
        self._session.cookies.set("d2lSessionVal", d2lsessionval)
        self._session.cookies.set("d2lSecureSessionVal", d2lsecuresessionval)

    # Auth
    def get_access_token(self):
        return AuthResponse(**self._session.post("/d2l/lp/auth/oauth2/token", {"scope": "*:*:*"}))

    # Root
    def get_my_enrollments(self):
        return self._session.get(f"/d2l/api/lp/{self._version}/enrollments/myenrollments/")

    # Organization a.k.a Course
    def get_users_in_org(self, org_unit_id: int):
        return self._session.get(f"/d2l/api/lp/{self._version}/enrollments/orgUnits/{org_unit_id}/users/")

    # Grades
    def get_student_grades_for_assessment(self, org_unit_id: int, assessment_id: int):
        return self._session.get(f"/d2l/api/le/{self._version}/{org_unit_id}/grades/{assessment_id}/values/")

    # Course Content
    def get_course_content(self, org_unit_id: int):
        return list(map(lambda module: ModuleResponse(**module),
                        self._session.get(f"/d2l/api/le/{self._version}/{org_unit_id}/content/root/")))

    def get_attachment_for_content(self, org_unit_id: int, topic_id: int):
        return self._session.get(f"/d2l/api/le/{self._version}/{org_unit_id}/content/topics/{topic_id}/file/")
