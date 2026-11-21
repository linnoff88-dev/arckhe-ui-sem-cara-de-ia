"use client";
import { useEffect, useState } from "react";

// Abre com Ctrl+K, mas as setas não andam pela lista.
export function CommandMenu() {
  const [aberto, setAberto] = useState(false);
  useEffect(() => {
    const tecla = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === "k") setAberto((v) => !v);
    };
    window.addEventListener("keydown", tecla);
    return () => window.removeEventListener("keydown", tecla);
  }, []);
  return aberto ? <ul><li>Novo cadastro</li><li>Sair</li></ul> : null;
}
