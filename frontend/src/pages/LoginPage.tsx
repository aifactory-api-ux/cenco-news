import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import { tokens } from '../styles/tokens';
import { apiFetch } from '../lib/api';

interface LoginFormInputs {
  email: string;
  password: string;
}

export default function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<LoginFormInputs>();

  const navigate = useNavigate();

  async function onSubmit(data: LoginFormInputs) {
    try {
      const res = await apiFetch('/api/v1/auth/login', {
        method: 'POST',
        body: JSON.stringify(data),
      });

      if ('access_token' in res) {
        localStorage.setItem('token', res.access_token);
        navigate('/');
      } else {
        setError('email', { type: 'manual', message: 'Credenciales inválidas' });
      }
    } catch (e) {
      setError('email', { type: 'manual', message: (e as Error).message || 'Error en inicio de sesión' });
    }
  }

  return (
    <div
      className="min-h-screen flex flex-col justify-center px-4 sm:px-6 lg:px-8"
      style={{ backgroundColor: tokens.colors.light_blue_background, fontFamily: tokens.typography.font_family }}
    >
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2
          className="mt-6 text-center font-semibold"
          style={{ fontSize: tokens.typography.h2.font_size, lineHeight: tokens.typography.h2.line_height, color: tokens.colors.primary_blue }}
        >
          Iniciar sesión en CENCO NEWS
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md bg-white rounded-md p-8 shadow-md">
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <Input
            id="email"
            type="email"
            label="Correo electrónico"
            {...register('email', {
              required: 'El correo electrónico es obligatorio',
              pattern: {
                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Correo electrónico inválido',
              },
            })}
            error={errors.email?.message}
            autoComplete="email"
          />

          <Input
            id="password"
            type="password"
            label="Contraseña"
            {...register('password', { required: 'La contraseña es obligatoria' })}
            error={errors.password?.message}
            autoComplete="current-password"
          />

          <div className="mt-6">
            <Button type="submit" disabled={isSubmitting} variant="primary">
              {isSubmitting ? 'Iniciando sesión...' : 'Iniciar sesión'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
