
-- Re-inserir usuários que falharam por causa do encoding
INSERT INTO usuarios (id_usuario, nome, id_escola, id_cidade) VALUES 
('user_001', 'Alice Ferreira', 1, 1),
('user_002', 'Bruno Gagliasso', 1, 1),
('user_003', 'Carla Diaz', 2, 1),
('user_004', 'Diego Alemao', 3, 1),
('user_005', 'Elena Gilbert', 4, 2),
('user_006', 'Fabio Assuncao', 5, 3),
('user_007', 'Gisele Bundchen', 6, 4),
('user_008', 'Heloisa Perisse', 1, 1),
('user_009', 'Italo Ferreira', 2, 1),
('user_010', 'Juliana Paes', 3, 1),
('user_011', 'Kevinho', 5, 3),
('user_012', 'Luan Santana', 5, 3),
('user_013', 'Marilia Mendonca', 6, 5),
('user_014', 'Neymar Jr', 6, 5);

-- Adicionar erros extras para o dashboard (especialmente ISS)
INSERT INTO eventos (id_atividade, tipo_evento, timestamp, dados_especificos) VALUES
('act_101', 'erro', NOW() - INTERVAL '1 hour', '{"assunto_pedagogico": "ISS"}'),
('act_103', 'erro', NOW() - INTERVAL '2 hours', '{"assunto_pedagogico": "ISS"}'),
('act_113', 'erro', NOW() - INTERVAL '3 hours', '{"assunto_pedagogico": "ISS"}');

-- Adicionar mais tentativas para o gráfico de engajamento/assiduidade
INSERT INTO eventos (id_atividade, tipo_evento, timestamp, dados_especificos) VALUES
('act_101', 'tentativa', NOW() - INTERVAL '10 minutes', '{}'),
('act_102', 'tentativa', NOW() - INTERVAL '20 minutes', '{}'),
('act_105', 'tentativa', NOW() - INTERVAL '30 minutes', '{}'),
('act_107', 'tentativa', NOW() - INTERVAL '40 minutes', '{}'),
('act_109', 'tentativa', NOW() - INTERVAL '50 minutes', '{}'),
('act_111', 'tentativa', NOW() - INTERVAL '60 minutes', '{}'),
('act_115', 'tentativa', NOW() - INTERVAL '70 minutes', '{}');

-- Garantir que as atividades tenham data_inicio recente para aparecerem no filtro de 7 dias
UPDATE atividades SET data_inicio = NOW() - (NOW() - data_inicio) * 0.1;
