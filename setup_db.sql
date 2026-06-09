-- 1. Garantir que as colunas JSON sejam JSONB (necessário para os filtros do dashboard)
ALTER TABLE eventos ALTER COLUMN dados_especificos SET DATA TYPE jsonb USING dados_especificos::jsonb;

-- 2. Limpeza Total de Dados para evitar duplicados e lixo de testes anteriores
TRUNCATE eventos, atividades, usuarios, escolas, cidades RESTART IDENTITY CASCADE;

-- 3. População de Cidades
INSERT INTO cidades (nome) VALUES 
('Cuiabá'), ('Várzea Grande'), ('Sinop'), ('Santo Antônio'), ('Rondonópolis');

-- 4. População de Escolas
INSERT INTO escolas (nome, id_cidade) VALUES 
('Escola Santa Maria', 1), 
('Colégio Dom Bosco', 1), 
('CEFET-MT', 1), 
('Instituto Federal', 2),
('Escola Estadual Tancredo Neves', 3),
('Escola Técnica Estadual', 4);

-- 5. População de Usuários
INSERT INTO usuarios (id_usuario, nome, id_escola, id_cidade) VALUES 
('user_001', 'Alice Ferreira', 1, 1),
('user_002', 'Bruno Gagliasso', 1, 1),
('user_003', 'Carla Diaz', 2, 1),
('user_004', 'Diego Alemão', 3, 1),
('user_005', 'Elena Gilbert', 4, 2),
('user_006', 'Fabio Assunção', 5, 3),
('user_007', 'Gisele Bündchen', 6, 4),
('user_008', 'Heloísa Perissé', 1, 1),
('user_009', 'Ítalo Ferreira', 2, 1),
('user_010', 'Juliana Paes', 3, 1),
('user_011', 'Kevinho', 5, 3),
('user_012', 'Luan Santana', 5, 3),
('user_013', 'Marília Mendonça', 6, 5),
('user_014', 'Neymar Jr', 6, 5);

-- 6. População de Atividades
INSERT INTO atividades (id_atividade, id_usuario, ferramenta, dispositivo, data_inicio) VALUES
('act_101', 'user_001', 'Aventura Fiscal', 'Desktop', NOW() - INTERVAL '2 days'),
('act_102', 'user_001', 'Palavras Cruzadas', 'Mobile', NOW() - INTERVAL '1 day'),
('act_103', 'user_002', 'Aventura Fiscal', 'Tablet', NOW() - INTERVAL '3 days'),
('act_104', 'user_003', 'Palavras Mágicas', 'Desktop', NOW() - INTERVAL '5 hours'),
('act_105', 'user_004', 'Pequeno Grande Cidadão', 'Mobile', NOW() - INTERVAL '1 hour'),
('act_106', 'user_005', 'Aventura Fiscal', 'Desktop', NOW() - INTERVAL '4 days'),
('act_107', 'user_006', 'Palavras Cruzadas', 'Mobile', NOW() - INTERVAL '2 days'),
('act_108', 'user_007', 'Aventura Fiscal', 'Tablet', NOW() - INTERVAL '6 days'),
('act_109', 'user_008', 'Pequeno Grande Cidadão', 'Desktop', NOW() - INTERVAL '12 hours'),
('act_110', 'user_009', 'Palavras Mágicas', 'Mobile', NOW() - INTERVAL '30 minutes'),
('act_111', 'user_011', 'Aventura Fiscal', 'Desktop', NOW() - INTERVAL '1 day'),
('act_112', 'user_012', 'Palavras Cruzadas', 'Mobile', NOW() - INTERVAL '2 days'),
('act_113', 'user_013', 'Pequeno Grande Cidadão', 'Desktop', NOW() - INTERVAL '3 days'),
('act_114', 'user_014', 'Palavras Cruzadas', 'Tablet', NOW() - INTERVAL '4 days'),
('act_115', 'user_003', 'Palavras Mágicas', 'Desktop', NOW() - INTERVAL '10 minutes');

-- 7. População de Eventos
INSERT INTO eventos (id_atividade, tipo_evento, timestamp, dados_especificos) VALUES
-- Atividade 101: 3 acertos, 1 erro, finalizada
('act_101', 'acerto', NOW() - INTERVAL '47 hours', '{"assunto_pedagogico": "ICMS"}'),
('act_101', 'acerto', NOW() - INTERVAL '46 hours', '{"assunto_pedagogico": "ISS"}'),
('act_101', 'erro', NOW() - INTERVAL '45 hours', '{"assunto_pedagogico": "IPTU"}'),
('act_101', 'acerto', NOW() - INTERVAL '44 hours', '{"assunto_pedagogico": "IPTU"}'),
('act_101', 'finalizacao', NOW() - INTERVAL '43 hours', '{}'),

-- Garantir erro no IPVA
('act_103', 'erro', NOW() - INTERVAL '70 hours', '{"assunto_pedagogico": "IPVA"}'),
('act_114', 'erro', NOW() - INTERVAL '3 days 23 hours', '{"assunto_pedagogico": "IPVA"}'),

-- Atividade 106: Instituto Federal (Várzea Grande)
('act_106', 'acerto', NOW() - INTERVAL '3 days 23 hours', '{"assunto_pedagogico": "ICMS"}'),
('act_106', 'acerto', NOW() - INTERVAL '3 days 22 hours', '{"assunto_pedagogico": "IPVA"}'),
('act_106', 'finalizacao', NOW() - INTERVAL '3 days 21 hours', '{}'),

-- Atividade 107: Sinop
('act_107', 'acerto', NOW() - INTERVAL '1 day 23 hours', '{"assunto_pedagogico": "IPTU"}'),
('act_107', 'finalizacao', NOW() - INTERVAL '1 day 22 hours', '{}'),

-- Atividade 108: Santo Antônio
('act_108', 'acerto', NOW() - INTERVAL '5 days 23 hours', '{"assunto_pedagogico": "ISS"}'),
('act_108', 'acerto', NOW() - INTERVAL '5 days 22 hours', '{"assunto_pedagogico": "ICMS"}'),
('act_108', 'finalizacao', NOW() - INTERVAL '5 days 21 hours', '{}'),

-- Atividades Rondonópolis
('act_113', 'acerto', NOW() - INTERVAL '2 days 23 hours', '{"assunto_pedagogico": "ISS"}'),
('act_113', 'finalizacao', NOW() - INTERVAL '2 days 22 hours', '{}'),
('act_114', 'acerto', NOW() - INTERVAL '3 days 22 hours', '{"assunto_pedagogico": "IPVA"}'),
('act_114', 'finalizacao', NOW() - INTERVAL '3 days 21 hours', '{}'),

-- Atividade 111
('act_111', 'acerto', NOW() - INTERVAL '23 hours', '{"assunto_pedagogico": "ICMS"}'),
('act_111', 'erro', NOW() - INTERVAL '22 hours', '{"assunto_pedagogico": "ICMS"}');

-- Adicionar tentativas separadamente (Corrigindo o ponto e vírgula ausente antes deste INSERT)
INSERT INTO eventos (id_atividade, tipo_evento, timestamp, dados_especificos) VALUES
('act_101', 'tentativa', NOW() - INTERVAL '47 hours 30 minutes', '{}'),
('act_102', 'tentativa', NOW() - INTERVAL '23 hours 30 minutes', '{}'),
('act_103', 'tentativa', NOW() - INTERVAL '71 hours 30 minutes', '{}'),
('act_104', 'tentativa', NOW() - INTERVAL '5 hours 30 minutes', '{}'),
('act_106', 'tentativa', NOW() - INTERVAL '3 days 23 hours 30 minutes', '{}');

-- Recentes com tempos e ações variadas
INSERT INTO eventos (id_atividade, tipo_evento, timestamp, dados_especificos) VALUES
('act_115', 'inicio', NOW() - INTERVAL '2 minutes', '{}'),
('act_110', 'acerto', NOW() - INTERVAL '18 minutes', '{"assunto_pedagogico": "IPTU"}'),
('act_105', 'acerto', NOW() - INTERVAL '42 minutes', '{"assunto_pedagogico": "ICMS"}'),
('act_104', 'finalizacao', NOW() - INTERVAL '3 hours 12 minutes', '{}'),
('act_109', 'erro', NOW() - INTERVAL '9 hours 45 minutes', '{"assunto_pedagogico": "IPTU"}');
