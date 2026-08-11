// src/pages/Login.tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/auth.service';
import { useAuthStore } from '../stores/auth.store';
import { tokens } from '../styles/tokens';

interface LoginFormInputs {
  email: string;
  password: string;
}

export default function Login() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormInputs>();

  const setToken = useAuthStore((state) => state.setToken);
  const navigate = useNavigate();

  async function onSubmit(data: LoginFormInputs) {
    try {
      const response = await login(data.email, data.password);
      setToken(response.access_token, '');
      navigate('/');
    } catch (error) {
      alert('Error al iniciar sesión');
    }
  }

  return (
    <div
      style={{
        backgroundColor: tokens.colors.light_blue_background.$value,
        fontFamily: tokens.typography.font_family.$value,
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <form
        onSubmit={handleSubmit(onSubmit)}
        style={{
          backgroundColor: tokens.colors.background_white.$value,
          padding: tokens.spacing.space_xl.$value,
          borderRadius: tokens.radii.radius_md.$value,
          boxShadow: tokens.shadows.shadow_md.$value,
          width: '360px',
          display: 'flex',
          flexDirection: 'column',
          gap: tokens.spacing.space_md.$value,
        }}
        noValidate
      >
        <h1
          style={{
            fontFamily: tokens.typography.font_family.$value,
            fontSize: tokens.typography.h1.font_size.$value,
            fontWeight: tokens.typography.h1.font_weight.$value,
            lineHeight: tokens.typography.h1.line_height.$value,
            marginBottom: tokens.spacing.space_md.$value,
            color: tokens.colors.primary_blue.$value,
          }}
        >
          Iniciar Sesión
        </h1>

        <div>
          <label htmlFor="email" style={{ fontWeight: '600' }}>
            Correo electrónico
          </label>
          <input
            id="email"
            type="email"
            {...register('email', {
              required: 'Correo electrónico es requerido',
              pattern: {
                value: /^[^@\s]+@[^@\s]+\.[^@\s]+$/,
                message: 'Formato de correo inválido',
              },
            })}
            style={{
              width: '100%',
              padding: tokens.spacing.space_sm.$value,
              borderRadius: tokens.radii.radius_sm.$value,
              border: `1px solid ${tokens.colors.secondary_text_border.$value}`,
              marginTop: tokens.spacing.space_xs.$value,
              fontSize: tokens.typography.body_regular.font_size.$value,
            }}
          />
          {errors.email && (
            <p style={{ color: tokens.colors.danger_red.$value, marginTop: '4px' }}>
              {errors.email.message}
            </p>
          )}
        </div>

        <div>
          <label htmlFor="password" style={{ fontWeight: '600' }}>
            Contraseña
          </label>
          <input
            id="password"
            type="password"
            {...register('password', {
              required: 'Contraseña es requerida',
              minLength: {
                value: 6,
                message: 'Debe tener al menos 6 caracteres',
              },
            })}
            style={{
              width: '100%',
              padding: tokens.spacing.space_sm.$value,
              borderRadius: tokens.radii.radius_sm.$value,
              border: `1px solid ${tokens.colors.secondary_text_border.$value}`,
              marginTop: tokens.spacing.space_xs.$value,
              fontSize: tokens.typography.body_regular.font_size.$value,
            }}
          />
          {errors.password && (
            <p style={{ color: tokens.colors.danger_red.$value, marginTop: '4px' }}>
              {errors.password.message}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          style={{
            backgroundColor: tokens.colors.primary_blue.$value,
            color: tokens.colors.background_white.$value,
            padding: tokens.spacing.space_sm.$value,
            borderRadius: tokens.radii.radius_md.$value,
            fontWeight: '600',
            cursor: 'pointer',
            marginTop: tokens.spacing.space_md.$value,
          }}
        >
          {isSubmitting ? 'Iniciando...' : 'Entrar'}
        </button>
      </form>
    </div>
  );
}
