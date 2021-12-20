export function getPersonFullName(person) {
  const { first_name: firstName, last_name: lastName, patr_name: patrName } = person;
  return `${lastName} ${firstName} ${patrName}`;
}

export function formatDate(date) {
  return date.toISOString().slice(0, 10);
}