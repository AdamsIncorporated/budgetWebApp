export function isPasswordComplex(password: string): boolean {
  if (password.length < 12 || password.length > 16) {
    return false;
  }

  let hasLowercase = false;
  let hasUppercase = false;
  let hasDigit = false;
  let hasSpecialChar = false;

  for (const char of password) {
    if (char >= "a" && char <= "z") {
      hasLowercase = true;
    } else if (char >= "A" && char <= "Z") {
      hasUppercase = true;
    } else if (char >= "0" && char <= "9") {
      hasDigit = true;
    } else if (["@", "$", "!", "%", "*", "?", "&"].includes(char)) {
      hasSpecialChar = true;
    }
  }

  return hasLowercase && hasUppercase && hasDigit && hasSpecialChar;
}

export const passwordErrorValidationMessage = `
Password must be between 12 and 16 charcters and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.`;
