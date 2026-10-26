-- WIQON · Sprint 3: favoritos y alertas de precio (proyecto Supabase ffswzcjcrxokoefhykvv)
-- Se pega una sola vez en Supabase → SQL Editor → Run. Se puede volver a correr sin romper nada.
--
-- Seguridad
--   · Row Level Security: cada usuario ve y cambia solo sus filas (auth.uid()).
--   · El navegador (clave anon + sesión) solo puede: crear una alerta, pausarla/reactivarla y borrarla.
--     Nunca puede marcarla como disparada ni leer el email de nadie.
--   · disparar_alerta / registrar_entrega / alerta_con_error: solo service_role (la credencial de n8n).
--   · Límites por usuario: 30 favoritos y 10 alertas activas.
--   · Solo monedas del catálogo (pares USDT de Binance, verificados el 2026-10-26).

-- ------------------------------------------------------------------ catálogo
create or replace function public.simbolo_valido(s text) returns boolean
language sql immutable set search_path = '' as $$
  select s = any (array['BTC','ETH','SOL','BNB','XRP','DOGE','ADA','AVAX','LINK','DOT','TRX','TON','LTC','BCH',
                        'SHIB','NEAR','UNI','ATOM','SUI','PEPE','ARB','OP','POL','APT','FIL','XLM','PAXG'])
$$;

-- ------------------------------------------------------------------ favoritos
create table if not exists public.favoritos (
  user_id uuid not null default auth.uid() references auth.users (id) on delete cascade,
  simbolo text not null check (public.simbolo_valido(simbolo)),
  creado  timestamptz not null default now(),
  primary key (user_id, simbolo)
);
alter table public.favoritos enable row level security;
drop policy if exists "favoritos: ver los propios" on public.favoritos;
drop policy if exists "favoritos: agregar propios" on public.favoritos;
drop policy if exists "favoritos: quitar propios" on public.favoritos;
create policy "favoritos: ver los propios" on public.favoritos for select to authenticated using (user_id = (select auth.uid()));
create policy "favoritos: agregar propios" on public.favoritos for insert to authenticated with check (user_id = (select auth.uid()));
create policy "favoritos: quitar propios" on public.favoritos for delete to authenticated using (user_id = (select auth.uid()));
revoke all on public.favoritos from anon, authenticated;
grant select, delete on public.favoritos to authenticated;
grant insert (simbolo) on public.favoritos to authenticated;

-- ------------------------------------------------------------------ alertas
create table if not exists public.alertas (
  id             bigint generated always as identity primary key,
  user_id        uuid not null default auth.uid() references auth.users (id) on delete cascade,
  simbolo        text not null check (public.simbolo_valido(simbolo)),
  tipo           text not null check (tipo in ('sobre', 'bajo', 'sube_pct', 'baja_pct')),
  valor          numeric not null check (valor > 0),
  idioma         text not null default 'es' check (idioma in ('es', 'pt', 'en')),
  estado         text not null default 'activa' check (estado in ('activa', 'pausada', 'disparada', 'error')),
  creada         timestamptz not null default now(),
  disparada      timestamptz,
  precio_disparo numeric,
  aviso          text,
  constraint pct_razonable check (tipo in ('sobre', 'bajo') or valor <= 100)
);
create index if not exists alertas_activas on public.alertas (estado) where estado = 'activa';
create index if not exists alertas_usuario on public.alertas (user_id);
alter table public.alertas enable row level security;
drop policy if exists "alertas: ver las propias" on public.alertas;
drop policy if exists "alertas: crear propias" on public.alertas;
drop policy if exists "alertas: cambiar propias" on public.alertas;
drop policy if exists "alertas: borrar propias" on public.alertas;
create policy "alertas: ver las propias" on public.alertas for select to authenticated using (user_id = (select auth.uid()));
create policy "alertas: crear propias" on public.alertas for insert to authenticated
  with check (user_id = (select auth.uid()) and estado = 'activa');
create policy "alertas: cambiar propias" on public.alertas for update to authenticated
  using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()) and estado in ('activa', 'pausada'));
create policy "alertas: borrar propias" on public.alertas for delete to authenticated using (user_id = (select auth.uid()));
revoke all on public.alertas from anon, authenticated;
grant select, delete on public.alertas to authenticated;
grant insert (simbolo, tipo, valor, idioma) on public.alertas to authenticated;
grant update (estado) on public.alertas to authenticated;

-- historial de disparos y de la entrega del email (lo escribe n8n; el usuario solo lo lee)
create table if not exists public.alertas_eventos (
  id         bigint generated always as identity primary key,
  alerta_id  bigint not null references public.alertas (id) on delete cascade,
  user_id    uuid not null references auth.users (id) on delete cascade,
  simbolo    text not null,
  tipo       text not null,
  valor      numeric not null,
  precio     numeric not null,
  cambio_24h numeric,
  disparada  timestamptz not null default now(),
  entrega    text not null default 'pendiente' check (entrega in ('pendiente', 'enviada', 'error')),
  detalle    text,
  entregada  timestamptz
);
create index if not exists eventos_usuario on public.alertas_eventos (user_id, disparada desc);
alter table public.alertas_eventos enable row level security;
drop policy if exists "eventos: ver los propios" on public.alertas_eventos;
create policy "eventos: ver los propios" on public.alertas_eventos for select to authenticated using (user_id = (select auth.uid()));
revoke all on public.alertas_eventos from anon, authenticated;
grant select on public.alertas_eventos to authenticated;

-- ------------------------------------------------------------------ límites y reactivación
create or replace function public.controlar_limites() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if tg_table_name = 'favoritos' then
    if (select count(*) from public.favoritos where user_id = new.user_id) >= 30 then
      raise exception 'limite_favoritos' using hint = 'Máximo 30 favoritos por cuenta';
    end if;
    return new;
  end if;
  -- alertas: al crearla o reactivarla
  if new.estado = 'activa' and (tg_op = 'INSERT' or old.estado <> 'activa') then
    if (select count(*) from public.alertas where user_id = new.user_id and estado = 'activa' and id <> new.id) >= 10 then
      raise exception 'limite_alertas' using hint = 'Máximo 10 alertas activas por cuenta';
    end if;
    if tg_op = 'UPDATE' then   -- reactivada: se borra el disparo anterior (queda en alertas_eventos)
      new.disparada := null; new.precio_disparo := null; new.aviso := null;
    end if;
  end if;
  return new;
end $$;
drop trigger if exists favoritos_limite on public.favoritos;
create trigger favoritos_limite before insert on public.favoritos for each row execute function public.controlar_limites();
drop trigger if exists alertas_limite on public.alertas;
create trigger alertas_limite before insert or update of estado on public.alertas for each row execute function public.controlar_limites();

-- ------------------------------------------------------------------ funciones para n8n (solo service_role)
-- Dispara una alerta una sola vez: si dos corridas llegan a la vez, solo una encuentra estado = 'activa'.
create or replace function public.disparar_alerta(p_id bigint, p_precio numeric, p_cambio numeric)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare a public.alertas; ev bigint; correo text;
begin
  update public.alertas set estado = 'disparada', disparada = now(), precio_disparo = p_precio, aviso = null
   where id = p_id and estado = 'activa' returning * into a;
  if not found then return jsonb_build_object('evento', null); end if;
  select email into correo from auth.users where id = a.user_id;
  insert into public.alertas_eventos (alerta_id, user_id, simbolo, tipo, valor, precio, cambio_24h)
       values (a.id, a.user_id, a.simbolo, a.tipo, a.valor, p_precio, p_cambio) returning id into ev;
  return jsonb_build_object('evento', ev, 'alerta', a.id, 'email', correo, 'idioma', a.idioma, 'simbolo', a.simbolo,
                            'tipo', a.tipo, 'valor', a.valor, 'precio', p_precio, 'cambio', p_cambio, 'disparada', a.disparada);
end $$;

create or replace function public.registrar_entrega(p_evento bigint, p_ok boolean, p_detalle text)
returns void language plpgsql security definer set search_path = '' as $$
declare aid bigint;
begin
  update public.alertas_eventos set entrega = case when p_ok then 'enviada' else 'error' end,
         detalle = left(p_detalle, 300), entregada = now()
   where id = p_evento returning alerta_id into aid;
  if not p_ok then
    update public.alertas set estado = 'error', aviso = 'No pudimos enviar el email de esta alerta.' where id = aid;
  end if;
end $$;

create or replace function public.alerta_con_error(p_id bigint, p_aviso text)
returns void language sql security definer set search_path = '' as $$
  update public.alertas set estado = 'error', aviso = left(p_aviso, 300) where id = p_id and estado = 'activa';
$$;

revoke all on function public.disparar_alerta(bigint, numeric, numeric) from public, anon, authenticated;
revoke all on function public.registrar_entrega(bigint, boolean, text) from public, anon, authenticated;
revoke all on function public.alerta_con_error(bigint, text) from public, anon, authenticated;
revoke all on function public.controlar_limites() from public, anon, authenticated;
grant execute on function public.disparar_alerta(bigint, numeric, numeric) to service_role;
grant execute on function public.registrar_entrega(bigint, boolean, text) to service_role;
grant execute on function public.alerta_con_error(bigint, text) to service_role;
