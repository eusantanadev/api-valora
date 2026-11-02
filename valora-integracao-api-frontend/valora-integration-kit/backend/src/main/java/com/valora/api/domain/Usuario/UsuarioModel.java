package com.valora.api.domain.Usuario;

import com.valora.api.domain.Endereco.Endereco;
import jakarta.persistence.*;
import lombok.*;
import org.jspecify.annotations.Nullable;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Collection;
import java.util.List;

@Table(name="T_VLR_USUARIO")
@Entity
@Getter
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
public class UsuarioModel implements UserDetails {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID_USUARIO")
    private Long id;

    @Column(name = "NM_USUARIO", nullable = false, length = 100)
    private String nome;

    @Column(name = "NR_TELEFONE", nullable = false, length = 20)
    private String telefone;

    @Column(name = "DS_EMAIL", nullable = false, length = 100, unique = true)
    private String email;

    @Column(name = "DS_SENHA_HASH", nullable = false)
    private String senha;

    @Column(name = "NR_CPF", nullable = false, length = 11, unique = true)
    private String cpf;

    @Column(name = "DT_NASCIMENTO", nullable = false)
    private LocalDate dataNascimento;

    @Embedded
    private Endereco endereco;

    @Column(name = "DT_CRIACAO", insertable = false, updatable = false)
    private LocalDateTime dataCriacao;

    @Column(name = "ST_ATIVO", nullable = false, insertable = false, length = 1)
    private Boolean ativo;

    public void setSenha(String senha) {
        this.senha = senha;
    }

    public UsuarioModel(CadastroUsuarioDTO cadastroUsuarioDTO) {
        this.ativo = true;
        this.nome = cadastroUsuarioDTO.nome();
        this.telefone = cadastroUsuarioDTO.telefone();
        this.email = cadastroUsuarioDTO.email();
        this.senha = cadastroUsuarioDTO.senha();
        this.cpf = cadastroUsuarioDTO.cpf();
        this.dataNascimento = cadastroUsuarioDTO.dataNascimento();
        this.endereco = new Endereco(cadastroUsuarioDTO.endereco());
    }

    public void atualizarInformacoes(AtualizaUsuarioDTO novoUsuarioDTO) {
        if(novoUsuarioDTO.nome() != null)
            this.nome = novoUsuarioDTO.nome();
        if(novoUsuarioDTO.telefone() != null)
            this.telefone = novoUsuarioDTO.telefone();
        if(novoUsuarioDTO.endereco() != null)
            this.endereco.atualizarInformacoes(novoUsuarioDTO.endereco());
    }

    public void desativar() {
        this.ativo = false;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return List.of(new SimpleGrantedAuthority("ROLE_USER"));
    }

    @Override
    public @Nullable String getPassword() {
        return this.senha;
    }

    @Override
    public String getUsername() {
        return this.email;
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }
}
