package com.valora.api.controller;

import com.valora.api.domain.Categoria.CategoriaDTO;
import com.valora.api.domain.Categoria.CategoriaModel;
import com.valora.api.domain.Categoria.CategoriaResponseDTO;
import com.valora.api.domain.Usuario.UsuarioModel;
import com.valora.api.service.CategoriaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/categorias")
public class CategoriaController {

    @Autowired
    private CategoriaService service;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CategoriaResponseDTO salvar(
            @RequestBody CategoriaDTO dto,
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        // O ID do proprietário vem do JWT; não confiamos em idUsuario enviado pelo browser.
        var seguro = new CategoriaDTO(null, usuario.getId(), dto.nmCategoria());
        return new CategoriaResponseDTO(service.salvar(seguro));
    }

    @GetMapping
    @ResponseStatus(HttpStatus.OK)
    public List<CategoriaResponseDTO> listarMinhas(
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        return service.listarPorUsuario(usuario.getId())
                .stream().map(CategoriaResponseDTO::new).toList();
    }

    @GetMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public CategoriaResponseDTO buscarPorId(
            @PathVariable Long id,
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        return new CategoriaResponseDTO(buscarDoUsuario(id, usuario));
    }

    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public CategoriaResponseDTO atualizar(
            @PathVariable Long id,
            @RequestBody CategoriaDTO dto,
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        buscarDoUsuario(id, usuario);
        var seguro = new CategoriaDTO(id, usuario.getId(), dto.nmCategoria());
        return new CategoriaResponseDTO(service.atualizar(id, seguro));
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void excluir(
            @PathVariable Long id,
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        buscarDoUsuario(id, usuario);
        service.excluir(id);
    }

    private CategoriaModel buscarDoUsuario(Long id, UsuarioModel usuario) {
        var categoria = service.buscarPorId(id);
        if (categoria.getUsuario() == null || !categoria.getUsuario().getId().equals(usuario.getId())) {
            throw new AccessDeniedException("Você não tem permissão para acessar esta categoria.");
        }
        return categoria;
    }
}
