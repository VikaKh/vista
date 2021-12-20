import React, { useState, useEffect } from "react";
import axios from "../utils/axios-config";
import Select from "react-select";
import { getAuthHeader } from "../utils/user";

const Search = ({
  value,
  resourceName,
  stringifyOption,
  onOptionSelect,
  placeholder,
  isClearable = false,
  queryParam = "full_name",
  extraQueryParams = null,
  sendInitialRequest = false,
}) => {
  const [searchString, setSearchString] = useState("");
  const [options, setOptions] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const onSearchChange = (value) => {
    setSearchString(value);
  };

  const onOptionChange = (option) => {
    onOptionSelect(option);
  };

  useEffect(() => {
    const queryOptions = async () => {
      setIsLoading(true);
      let params = extraQueryParams;
      if (params == null) {
        params = {};
      } 
      try {
        const response = await axios.get(`/${resourceName}/`, {
          params: { [queryParam]: searchString, ...params },
          headers: getAuthHeader(),
        });
        setOptions(response.data.map((record) => ({ value: record.id, label: stringifyOption(record) })));
        setIsLoading(false);
      } catch {
        setIsLoading(false);
        setOptions([]);
      }
    };
    if (searchString.length >= 3) {
      queryOptions();
    }
  }, [searchString, extraQueryParams, queryParam, resourceName, stringifyOption]);

  useEffect(() => {
    const sendRequest = async () => {
      setIsLoading(true);
      let params = extraQueryParams;
      if (params == null) {
        params = {};
      }
      try {
        const response = await axios.get(`/${resourceName}/`, {
          params: params,
          headers: getAuthHeader(),
        });
        setOptions(response.data.map((record) => ({ value: record.id, label: stringifyOption(record) })));
        setIsLoading(false);
      } catch {
        setIsLoading(false);
        setOptions([]);
      }
    };
    if (sendInitialRequest) {
      sendRequest();
    }
  }, [])

  return (
    <div>
      <Select
        isSearchable={true}
        isClearable={isClearable}
        value={value}
        onInputChange={onSearchChange}
        options={options}
        onChange={onOptionChange}
        isLoading={isLoading}
        placeholder={placeholder ? placeholder : "Поиск"}
      />
    </div> 
  );
};

export default Search;
