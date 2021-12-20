export const logout = () => {
  localStorage.clear();
  window.location.href = "/login";
};

export const getCurrentUser = () => {
  return Boolean(localStorage.getItem("token"));
};

export function getAuthHeader() {
  return { Authorization: `Token ${localStorage.getItem("token")}` };
}

export function setDataToLocalstorage(data) {
  const {
    token,
    first_name: firstName,
    last_name: lastName,
    patronymic,
    organisation: { id: orgId, full_name: orgName },
  } = data;
  localStorage.setItem("token", token);
  localStorage.setItem("firstName", firstName);
  localStorage.setItem("lastName", lastName);
  localStorage.setItem("patronymic", patronymic);
  localStorage.setItem("orgId", orgId);
  localStorage.setItem("orgName", orgName);
}
