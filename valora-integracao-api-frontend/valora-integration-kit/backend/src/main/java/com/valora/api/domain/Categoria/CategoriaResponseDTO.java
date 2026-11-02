package com.valora.api.domain.Categoria;

import java.time.LocalDate;

/** Resposta pública da categoria: não serializa UsuarioModel nem seus dados sensíveis. */
public record CategoriaResponseDTO(
        Long idCategoria,
        Long idUsuario,
        String nmCategoria,
        LocalDate dtCriacao
) {
    public CategoriaResponseDTO(CategoriaModel categoria) {
        this(
                categoria.getIdCategoria(),
                categoria.getUsuario().getId(),
                categoria.getNmCategoria(),
                categoria.getDtCriacao()
        );
    }
}
