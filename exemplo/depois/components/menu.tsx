"use client";
import { Drawer } from "vaul";

// A gaveta acompanha o dedo e fecha ao ser puxada para baixo.
export function Menu() {
  return (
    <Drawer.Root>
      <Drawer.Trigger>Menu</Drawer.Trigger>
      <Drawer.Portal>
        <Drawer.Content>
          <Drawer.Title>Opções</Drawer.Title>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
