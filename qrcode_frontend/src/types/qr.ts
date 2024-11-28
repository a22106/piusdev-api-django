export interface InputField {
    name: string;
    type: string;
    label: string;
    required?: boolean;
    options?: SelectOption[];
    step?: string;
    min?: number;
    max?: number;
  }

  export interface SelectOption {
    value: string;
    label: string;
  }

  export interface QRType {
    value: string;
    label: string;
  }

  export interface FormData {
    [key: string]: string;
  }