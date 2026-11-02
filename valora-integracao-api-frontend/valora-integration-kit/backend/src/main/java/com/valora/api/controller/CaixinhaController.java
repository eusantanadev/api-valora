package com.valora.api.controller;

import com.valora.api.domain.Caixinha.CaixinhaDTO;
import com.valora.api.domain.Caixinha.CaixinhaModel;
import com.valora.api.domain.Caixinha.CaixinhaResponseDTO;
import com.valora.api.domain.Usuario.UsuarioModel;
import com.valora.api.service.CaixinhaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/caixinhas")
public class CaixinhaController {

    @Autowired
    private CaixinhaService service;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public CaixinhaResponseDTO salvar(
            @RequestBody CaixinhaDTO dto,
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        // O usuário associado à caixinha é sempre o dono autenticado.
        var seguro = new CaixinhaDTO(null, usuario.getId(), dto.nmCaixinha(), dto.vlMeta(), dto.vlAtual());
        return new CaixinhaResponseDTO(service.salvar(seguro));
    }

    @GetMapping
    @ResponseStatus(HttpStatus.OK)
    public List<CaixinhaResponseDTO> listarMinhas(
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        return service.listarPorUsuario(usuario.getId())
                .stream().map(CaixinhaResponseDTO::new).toList();
    }

    @GetMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public CaixinhaResponseDTO buscarPorId(
            @PathVariable Long id,
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        return new CaixinhaResponseDTO(buscarDoUsuario(id, usuario));
    }

    @PutMapping("/{id}")
    @ResponseStatus(HttpStatus.OK)
    public CaixinhaResponseDTO atualizar(
            @PathVariable Long id,
            @RequestBody CaixinhaDTO dto,
            @AuthenticationPrincipal UsuarioModel usuario
    ) {
        buscarDoUsuario(id, usuario);
        var seguro = new CaixinhaDTO(id, usuario.getId(), dto.nmCaixinha(), dto.vlMeta(), dto.vlAtual());
        return new CaixinhaResponseDTO(service.atualizar(id, seguro));
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

    private CaixinhaModel buscarDoUsuario(Long id, UsuarioModel usuario) {
        var caixinha = service.buscarPorId(id);
        if (caixinha.getUsuario() == null || !caixinha.getUsuario().getId().equals(usuario.getId())) {
            throw new AccessDeniedException("Você não tem permissão para acessar esta caixinha.");
        }
        return caixinha;
    }
}
