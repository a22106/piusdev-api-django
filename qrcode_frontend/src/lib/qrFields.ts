import type { InputField, QRType } from "../types/qr";

export const QR_TYPES: QRType[] = [
  { value: "url", label: "URL" },
  { value: "text", label: "Text" },
  { value: "email", label: "Email" },
  { value: "phone", label: "Phone Number" },
  { value: "sms", label: "SMS" },
  { value: "wifi", label: "WiFi" },
  { value: "vcard", label: "VCard" },
  { value: "mecard", label: "MeCard" },
  { value: "geo", label: "Location" },
  { value: "event", label: "Event" },
  { value: "bitcoin", label: "Bitcoin" },
  { value: "whatsapp", label: "WhatsApp" },
];

export function getInputFields(selectedType: string): InputField[] {
  switch (selectedType) {
    case "url":
      return [
        {
          name: "url",
          type: "text",
          label: "URL",
          required: true,
        },
      ];

    case "text":
      return [
        {
          name: "text",
          type: "textarea",
          label: "Text",
          required: true,
        },
      ];

    case "email":
      return [
        {
          name: "email",
          type: "email",
          label: "Email Address",
          required: true,
        },
        {
          name: "subject",
          type: "text",
          label: "Subject",
        },
        {
          name: "body",
          type: "textarea",
          label: "Message Body",
        },
      ];

    case "phone":
      return [
        {
          name: "phone",
          type: "tel",
          label: "Phone Number",
          required: true,
        },
      ];

    case "vcard":
      return [
        {
          name: "first_name",
          type: "text",
          label: "First Name",
          required: true,
        },
        {
          name: "last_name",
          type: "text",
          label: "Last Name",
          required: true,
        },
        {
          name: "phone",
          type: "tel",
          label: "Phone Number",
        },
        {
          name: "mobile",
          type: "tel",
          label: "Mobile Number",
          required: true,
        },
        {
          name: "email",
          type: "email",
          label: "Email",
          required: true,
        },
        {
          name: "url",
          type: "url",
          label: "Website",
        },
        {
          name: "organization",
          type: "text",
          label: "Organization",
        },
      ];

    case "wifi":
      return [
        {
          name: "ssid",
          type: "text",
          label: "Network Name (SSID)",
          required: true,
        },
        {
          name: "password",
          type: "password",
          label: "Password",
        },
        {
          name: "encryption",
          type: "select",
          label: "Encryption",
          options: [
            { value: "WPA", label: "WPA/WPA2" },
            { value: "WEP", label: "WEP" },
            { value: "nopass", label: "None" },
          ],
          required: true,
        },
      ];

    case "sms":
      return [
        {
          name: "phone_number",
          type: "tel",
          label: "Phone Number",
          required: true,
        },
        {
          name: "message",
          type: "textarea",
          label: "Message",
        },
      ];

    case "geo":
      return [
        {
          name: "latitude",
          type: "number",
          label: "Latitude",
          required: true,
          step: "any",
        },
        {
          name: "longitude",
          type: "number",
          label: "Longitude",
          required: true,
          step: "any",
        },
        {
          name: "query",
          type: "text",
          label: "Place Name",
        },
      ];

    case "event":
      return [
        {
          name: "summary",
          type: "text",
          label: "Event Title",
          required: true,
        },
        {
          name: "start_date",
          type: "datetime-local",
          label: "Start Date",
          required: true,
        },
        {
          name: "end_date",
          type: "datetime-local",
          label: "End Date",
          required: true,
        },
        {
          name: "location",
          type: "text",
          label: "Location",
        },
        {
          name: "description",
          type: "textarea",
          label: "Description",
        },
      ];

    case "whatsapp":
      return [
        {
          name: "phone_number",
          type: "tel",
          label: "Phone Number",
          required: true,
        },
        {
          name: "message",
          type: "textarea",
          label: "Message",
        },
      ];

    case "bitcoin":
      return [
        {
          name: "address",
          type: "text",
          label: "Bitcoin Address",
          required: true,
        },
        {
          name: "amount",
          type: "number",
          label: "Amount (BTC)",
          step: "any",
        },
        {
          name: "label",
          type: "text",
          label: "Label",
        },
        {
          name: "message",
          type: "text",
          label: "Message",
        },
      ];

    default:
      return [];
  }
}
