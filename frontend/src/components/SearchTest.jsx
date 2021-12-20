import React, { useState } from "react";
import Search from "./Search";

const SearchTest = () => {
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [selectedPatient, setSelectedPatient] = useState(null);

  const stringifyEmployeeOption = (option) => {
    const {
      first_name: firstName,
      last_name: lastName,
      patr_name: patrName,
      organisation: { full_name: orgName },
    } = option;
    return `${lastName} ${firstName} ${patrName}, ${orgName}`;
  };

  const stringifyPatientOption = (option) => {
    const { first_name: firstName, last_name: lastName, patr_name: patrName } = option;
    return `${lastName} ${firstName} ${patrName}`;
  };

  console.log("in parent", selectedEmployee, selectedPatient);
  return (
    <div>
      <Search resourceName="employees" stringifyOption={stringifyEmployeeOption} onOptionSelect={setSelectedEmployee} />
      <Search resourceName="patients" stringifyOption={stringifyPatientOption} onOptionSelect={setSelectedPatient} />
    </div>
  );
};

export default SearchTest;
