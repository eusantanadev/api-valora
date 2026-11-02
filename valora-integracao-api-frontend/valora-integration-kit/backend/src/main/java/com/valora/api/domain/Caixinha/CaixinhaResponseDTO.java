package com.valora.api.domain.Caixinha;

import java.math.BigDecimal;
import java.time.LocalDate;

/** Resposta pública da caixinha: não serializa UsuarioModel nem seus dados sensíveis. */
public record CaixinhaResponseDTO(
        Long idCaixinha,
        Long idUsuario,
        String nmCaixinha,
        BigDecimal vlMeta,
        BigDecimal vlAtual,
        LocalDate dtCriacao
) {
    public CaixinhaResponseDTO(CaixinhaModel caixinha) {
        this(
                caixinha.getIdCaixinha(),
                caixinha.getUsuario().getId(),
                caixinha.getNmCaixinha(),
                caixinha.getVlMeta(),
                caixinha.getVlAtual(),
                caixinha.getDtCriacao()
        );
    }
}
