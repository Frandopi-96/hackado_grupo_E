// Utilidades comunes del frontend para hablar con la API del backend.
// El frontend nunca habla con la base de datos ni con la IA: solo con /api.

async function api(ruta, { metodo = "GET", datos } = {}) {
  const opciones = { method: metodo, credentials: "same-origin", headers: {} };
  if (datos !== undefined) {
    opciones.headers["Content-Type"] = "application/json";
    opciones.body = JSON.stringify(datos);
  }
  let respuesta;
  try {
    respuesta = await fetch("/api" + ruta, opciones);
  } catch {
    return { ok: false, status: 0, datos: null, error: "No hay conexión con el servidor." };
  }
  let cuerpo = null;
  try { cuerpo = await respuesta.json(); } catch { /* respuesta sin cuerpo */ }
  return {
    ok: respuesta.ok,
    status: respuesta.status,
    datos: cuerpo,
    error: respuesta.ok ? null : mensajeError(respuesta.status, cuerpo),
  };
}

// Convierte el error de la API en un mensaje en español para el alumno.
function mensajeError(status, cuerpo) {
  if (cuerpo && typeof cuerpo.detail === "string") return cuerpo.detail;
  if (status === 422) return "Revisa los datos: hay algún campo incompleto o no válido.";
  return "Ha ocurrido un error. Inténtalo de nuevo.";
}

// Lleva al alumno a la pantalla que le toca según su estado.
async function irSegunEstado() {
  const r = await api("/perfil");
  if (r.status === 401) location.href = "/login.html";
  else if (r.status === 404) location.href = "/formulario.html";
  else if (r.ok) location.href = "/itinerario.html";
}
