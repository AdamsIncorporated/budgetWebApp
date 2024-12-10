import React, { useState } from "react";

interface SelectProps {
  id: string;
  name: string;
  options: { value: string | number; label: string }[];
  defaultValue?: string | number;
  placeholder?: string;
  onChange?: (value: string | number) => void;
}

const SelectComponent: React.FC<SelectProps> = ({
  id,
  name,
  options,
  defaultValue,
  placeholder,
  onChange,
}) => {
  const [selectedValue, setSelectedValue] = useState<string | number>(
    defaultValue || ""
  );

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const newValue = event.target.value;
    setSelectedValue(newValue);
    onChange?.(newValue);
  };

  return (
    <select
      id={id}
      name={name}
      value={selectedValue}
      onChange={handleChange}
      className="bg-white border shadow-md text-stone-700 text-sm rounded-lg focus:ring-teal-500 focus:border-teal-500 block w-full p-2.5"
    >
      <option value="" disabled selected>
        {placeholder || "--Select--"}
      </option>
      {options.map((option) => (
        <option key={option.value} value={option.value} className="bg-white text-stone-500 ">
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default SelectComponent;
