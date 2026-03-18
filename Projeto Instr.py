import json
import re
import urllib.request
import ssl
import os

class GeminiAssistant:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        self.fullData = None
        self.quizData = None

    def _call_gemini(self, user_prompt, system_prompt=None):
        if not self.api_key:
            return None
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": user_prompt}]}]
        }
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(endpoint, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, context=ssl.create_default_context()) as resp:
                resp_data = resp.read()
                j = json.loads(resp_data.decode('utf-8'))
                text = j.get('candidates', [])[0].get('content', {}).get('parts', [])[0].get('text')
                return text
        except Exception:
            return None

    def _fallback_plan(self, task):
        oii = {
            "tarefa": f"Estudar {task}",
            "condicao": f"Condição padrão para instrução de {task}",
            "padrao": f"Conformidade com doutrina de instrução de {task}"
        }
        plano = {
            "introducao": f"Introdução ao tema {task}.",
            "desenvolvimento": [
                f"Conceitos-chave de {task}",
                f"Aplicação prática de {task}",
                f"Exemplo ilustrativo relacionado a {task}"
            ],
            "conclusao": f"Síntese dos pontos principais sobre {task}."
        }
        risco = {
            "perigos": [f"Interpretação incorreta do tema {task}", "Fatos desatualizados"],
            "medidas": [f"Verificar fontes oficiais sobre {task}", "Atualizar conteúdo regularmente"]
        }
        return {"oii": oii, "plano": plano, "risco": risco}

    def gerar_plano_ia(self, task):
        if not task:
            raise ValueError("Task is required")
        systemPrompt = "Você é um Instrutor Sênior do Exército. Gere planos de instrução. Responda APENAS em JSON."
        userPrompt = f'''Crie um plano detalhado para: "{task}".
        JSON Format:
        {{
            "oii": {{ "tarefa": "...", "condicao": "...", "padrao": "..." }},
            "plano": {{ "introducao": "...", "desenvolvimento": ["...", "..."], "conclusao": "..." }},
            "risco": {{ "perigos": ["...", "..."], "medidas": ["...", "..."] }}
        }}'''
        text = self._call_gemini(userPrompt, systemPrompt)
        if not text:
            self.fullData = self._fallback_plan(task)
            return self.fullData
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            try:
                self.fullData = json.loads(m.group(0))
                return self.fullData
            except json.JSONDecodeError:
                pass
        self.fullData = self._fallback_plan(task)
        return self.fullData

    def gerar_quiz_extra(self):
        if not self.fullData or 'plano' not in self.fullData:
            raise RuntimeError("Plano não gerado ainda")
        systemPrompt = "Você é um avaliador militar. Crie um questionário baseado no plano de instrução. Responda em JSON."
        userPrompt = f'''Com base neste plano: {json.dumps(self.fullData['plano'])}, crie 3 perguntas de múltipla escolha para verificar o aprendizado. 
        JSON format: {{"quiz": [{{"pergunta": "...", "opcoes": ["A","B","C","D"], "resposta": "A"}}]}}'''
        text = self._call_gemini(userPrompt, systemPrompt)
        if text:
            m = re.search(r'\{[\s\S]*\}', text)
            if m:
                try:
                    self.quizData = json.loads(m.group(0))
                    return self.quizData
                except json.JSONDecodeError:
                    pass
        self.quizData = {
            "quiz": [
                {"pergunta": "Qual é o objetivo principal da tarefa?", "opcoes": ["Conceito A","Conceito B","Conceito C","Conceito D"], "resposta": "A"},
                {"pergunta": "Qual é a etapa mais importante no desenvolvimento?", "opcoes": ["Etapa 1","Etapa 2","Etapa 3","Etapa 4"], "resposta": "B"},
                {"pergunta": "Qual medida de risco é usada para mitigação?", "opcoes": ["Medida A","Medida B","Medida C","Medida D"], "resposta": "C"}
            ]
        }
        return self.quizData

    def render_data(self, tab):
        if not self.fullData:
            return "Nenhum plano disponível. Gere um plano primeiro."
        if tab == 'oii':
            oii = self.fullData.get('oii', {})
            return f"Tarefa: {oii.get('tarefa','')}\nCondição: {oii.get('condicao','')}\nPadrão: {oii.get('padrao','')}"
        if tab == 'plano':
            plano = self.fullData.get('plano', {})
            introd = plano.get('introducao','')
            desenvolvimento = plano.get('desenvolvimento', [])
            conc = plano.get('conclusao','')
            dev_list = '\n'.join(['- '+d for d in desenvolvimento])
            return f"Introdução: {introd}\nDesenvolvimento:\n{dev_list}\nConclusão: {conc}"
        if tab == 'risco':
            risco = self.fullData.get('risco', {})
            perigos = risco.get('perigos', [])
            medidas = risco.get('medidas', [])
            p = '\n'.join(['- '+x for x in perigos])
            m = '\n'.join(['- '+x for x in medidas])
            return f"Perigos:\n{p}\nMedidas de Controle:\n{m}"
        if tab == 'quiz':
            q = self.quizData.get('quiz', []) if self.quizData else []
            if not q:
                return "Clique para gerar o questionário."
            lines = []
            for i,quest in enumerate(q,1):
                lines.append(f"Q{i}: {quest.get('pergunta','')}")
                opts = quest.get('opcoes', [])
                for opt in opts:
                    lines.append(f"   {opt}")
                lines.append(f"Resposta: {quest.get('resposta','')}")
            return '\n'.join(lines)
        return ""

def main():
    print("Gemini Assistente Militar - CLI")
    api_key = input("Insira a API key da Gemini (ou pressione Enter para uso offline): ").strip() or None
    app = GeminiAssistant(api_key=api_key)

    while True:
        print("\nMenu:")
        print("1) Gerar plano para uma tarefa")
        print("2) Mostrar OII (Tarefa)")
        print("3) Mostrar Plano de Sessão")
        print("4) Mostrar Riscos e Controles")
        print("5) Gerar Prova (Quiz) baseada no plano")
        print("6) Mostrar Quiz")
        print("7) Exportar Plano/Quiz como JSON")
        print("0) Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == '1':
            task = input("Informe a matéria/tarefa (Ex: Fuzil 7,62mm, Higiene, Orientação...): ").strip()
            if not task:
                print("Tarefa vazia.")
                continue
            app.gerar_plano_ia(task)
            print("Plano gerado.")
        elif choice == '2':
            print(app.render_data('oii'))
        elif choice == '3':
            print(app.render_data('plano'))
        elif choice == '4':
            print(app.render_data('risco'))
        elif choice == '5':
            try:
                app.gerar_quiz_extra()
                print("Quiz gerado.")
            except Exception as e:
                print("Erro ao gerar quiz:", e)
        elif choice == '6':
            print(app.render_data('quiz'))
        elif choice == '7':
            to_export = {
                "fullData": app.fullData,
                "quizData": app.quizData
            }
            with open("plane_quiz_export.json", "w", encoding="utf-8") as f:
                json.dump(to_export, f, ensure_ascii=False, indent=2)
            print("Exportado para plane_quiz_export.json")
        elif choice == '0':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()