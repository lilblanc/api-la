-- Popular Cidades
INSERT INTO cidades (nome) VALUES ('Cuiabá'), ('Várzea Grande'), ('Sinop'), ('Santo Antônio') ON CONFLICT (nome) DO NOTHING;

-- Popular Escolas (Assumindo IDs 1, 2, 3, 4 para as cidades acima)
INSERT INTO escolas (nome, id_cidade) VALUES 
('Escola Santa Maria', 1), 
('Colégio Dom Bosco', 1), 
('CEFET-MT', 1), 
('Instituto Federal', 2);

-- Popular alguns usuários para teste
-- Nota: id_usuario é string no modelo original
INSERT INTO usuarios (id_usuario, nome, id_escola, id_cidade) VALUES 
('estudante_1001', 'João Silva', 1, 1),
('estudante_1002', 'Maria Oliveira', 1, 1),
('estudante_1003', 'Pedro Souza', 2, 1),
('estudante_1004', 'Ana Costa', 3, 1),
('estudante_1005', 'Carlos Lima', 4, 2);

-- Atualizar atividades existentes para apontar para usuários válidos (opcional, para dados antigos)
-- UPDATE atividades SET id_usuario = 'estudante_1001' WHERE id_usuario NOT IN (SELECT id_usuario FROM usuarios);
