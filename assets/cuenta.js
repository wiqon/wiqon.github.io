// WIQON · cuentas de usuario con Supabase (ingreso por enlace al email, sin contraseña).
// La clave "anon" es pública por diseño. Esto ordena la experiencia (qué se ve con y sin cuenta);
// no protege datos secretos: todo lo que muestra la web es información pública.
(function () {
  const URL_SB = "https://ffswzcjcrxokoefhykvv.supabase.co";
  const ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmc3d6Y2pjcnhva29lZmh5a3Z2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE0MjA3NTUsImV4cCI6MjEwNjk5Njc1NX0.3hKqtMak_aoK4Hamv6NWzGZIURQ28yMh1nyGZtAHN4c";
  const PT = document.documentElement.lang.toLowerCase().startsWith("pt");
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const T = PT ? {
    enviando: "Enviando…", enviado: "Pronto! Enviamos um link para {e}. Abra o seu e-mail e toque no link para entrar (veja também o spam).",
    error: "Não foi possível enviar o link agora. Tente de novo em alguns minutos.", limite: "Muitas tentativas. Espere alguns minutos e tente de novo.",
    email: "Digite um e-mail válido.", privacidad: "Para criar a conta, aceite a política de privacidade.", salir: "Sair", enviar: "Enviar link de acesso",
  } : {
    enviando: "Enviando…", enviado: "¡Listo! Te enviamos un enlace a {e}. Abrí tu email y tocá el enlace para entrar (revisá también el spam).",
    error: "No pudimos enviar el enlace ahora. Probá de nuevo en unos minutos.", limite: "Demasiados intentos. Esperá unos minutos y probá de nuevo.",
    email: "Escribí un email válido.", privacidad: "Para crear la cuenta, aceptá la política de privacidad.", salir: "Salir", enviar: "Enviar enlace de acceso",
  };
  const dlg = $("#acceso");

  // ---------- abrir / cerrar la ventana de acceso ----------
  const abrir = (e) => { if (e) e.preventDefault(); if (dlg && !dlg.open) { dlg.showModal(); setTimeout(() => $("#acc-email").focus(), 50); } };
  $$("[data-acceso]").forEach((b) => b.addEventListener("click", abrir));
  if (dlg) {
    $(".cerrar", dlg).addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  }
  if (location.hash === "#ingresar") abrir();

  // ---------- estado de sesión ----------
  function pintarSesion(sesion) {
    const logueado = !!sesion;
    document.documentElement.classList.toggle("logueado", logueado);
    try { localStorage.setItem("wiqon-sesion", logueado ? "1" : "0"); } catch (e) { /* sin almacenamiento */ }
    const chip = $("#usuario");
    if (chip && logueado) {
      const email = sesion.user.email || "";
      $(".ini", chip).textContent = (email[0] || "W").toUpperCase();
      $(".ini", chip).title = email;
    }
    document.dispatchEvent(new CustomEvent("wiqon:sesion", { detail: { logueado } }));
  }

  if (!window.supabase) { pintarSesion(null); return; }
  const sb = window.supabase.createClient(URL_SB, ANON, { auth: { persistSession: true, detectSessionInUrl: true, flowType: "implicit" } });
  sb.auth.getSession().then(({ data }) => pintarSesion(data.session));
  sb.auth.onAuthStateChange((evento, sesion) => {
    pintarSesion(sesion);
    if (evento === "SIGNED_IN" && location.hash.includes("access_token")) history.replaceState(null, "", location.pathname);
    if (evento === "SIGNED_IN" && dlg && dlg.open) dlg.close();
  });
  const salir = $("#salir");
  if (salir) { salir.textContent = T.salir; salir.addEventListener("click", () => sb.auth.signOut()); }

  // ---------- enviar el enlace de acceso ----------
  const form = $("#acc-form");
  if (form) form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = $("#acc-email").value.trim(), msg = $("#acc-msg"), btn = $("button[type=submit]", form);
    msg.className = "msg"; msg.textContent = "";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.className = "msg error"; msg.textContent = T.email; return; }
    if (!$("#acc-priv").checked) { msg.className = "msg error"; msg.textContent = T.privacidad; return; }
    btn.disabled = true; btn.textContent = T.enviando;
    const { error } = await sb.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: location.origin + location.pathname,
        data: { acepta_novedades: $("#acc-nov").checked, idioma: PT ? "pt-BR" : "es", acepto_privacidad: new Date().toISOString() },
      },
    });
    btn.disabled = false; btn.textContent = T.enviar;
    if (error) {
      msg.className = "msg error";
      msg.textContent = /rate|limit|seconds/i.test(error.message) ? T.limite : T.error;
    } else {
      msg.className = "msg ok"; msg.textContent = T.enviado.replace("{e}", email);
      form.reset();
    }
  });
})();
