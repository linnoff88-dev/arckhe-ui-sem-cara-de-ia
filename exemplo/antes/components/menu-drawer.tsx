"use client";
import { useState } from "react";

// Abre e fecha, mas não acompanha o dedo.
export function MenuDrawer() {
  const [aberta, setAberta] = useState(false);
  return (
    <>
      <button onClick={() => setAberta(!aberta)}>Menu</button>
      {aberta && <aside className="fixed bottom-0 w-full">Opções</aside>}
    </>
  );
}
