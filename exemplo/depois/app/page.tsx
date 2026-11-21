"use client";
import { toast } from "sonner";
import { Meteors } from "../components/destaque";
import { Menu } from "../components/menu";
import { Busca } from "../components/busca";

export default function Cadastro() {
  return (
    <main>
      <Meteors />
      <h1>Cadastro</h1>
      <input aria-label="Nome" placeholder="Nome" />
      <input aria-label="E-mail" placeholder="E-mail" />
      <button onClick={() => toast.success("Cadastro salvo")}>Salvar</button>
      <Menu />
      <Busca />
    </main>
  );
}
