export type AuthUser = {
  id: number;
  fullName: string;
  email: string;
  isActive: boolean;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type RegisterPayload = {
  fullName: string;
  email: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: 'bearer';
};
