import type { FormData } from '../types/qr';

const API_BASE_URL = 'http://localhost:8000/v1/qr';  // TODO: prod 실제 서버 주소로 변경.

export async function generateQRCode(selectedType: string, formData: FormData): Promise<Blob> {
    const endpoint = `${API_BASE_URL}/${selectedType === 'phone' ? 'phonenumber' : selectedType}/`;
    const adjustedFormData = adjustFormData(selectedType, formData);

    const queryParams = new URLSearchParams(adjustedFormData).toString();
    const fullUrl = `${endpoint}?${queryParams}`;

    const response = await fetch(fullUrl);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to generate QR code: ${response.status} ${response.statusText}\n${errorText}`);
    }

    const blob = await response.blob();
    if (blob.size === 0) {
      throw new Error('Received empty response from server');
    }

    return blob;
  }

function adjustFormData(selectedType: string, formData: FormData): FormData {
    const adjustedFormData = { ...formData };

    switch (selectedType) {
      case 'phone':
        adjustedFormData.phone_number = formData.phone;
        delete adjustedFormData.phone;
        break;
      case 'vcard':
        adjustedFormData.vcard_phone = formData.phone;
        adjustedFormData.vcard_mobile = formData.mobile;
        adjustedFormData.vcard_email = formData.email;
        adjustedFormData.vcard_url = formData.url;
        break;
      case 'event':
        if (adjustedFormData.start_date) {
          adjustedFormData.start_date = new Date(adjustedFormData.start_date).toISOString();
        }
        if (adjustedFormData.end_date) {
          adjustedFormData.end_date = new Date(adjustedFormData.end_date).toISOString();
        }
        break;
    }

    return adjustedFormData;
}