import React, { useState } from 'react';
import { Steps } from './components/Steps';
import { StudentForm } from './components/StudentForm';
import { AssessmentForm } from './components/AssessmentForm';
import { AnalysisForm } from './components/AnalysisForm';
import { ReportResult } from './components/ReportResult';
import { ReportData, Step, StudentInfo, AssessmentData, ReportConfig } from './types';
import { generateReport } from './services/geminiService';
import { Brain } from 'lucide-react';

// Initial states
const initialStudent: StudentInfo = {
  name: '', age: '', grade: '', school: '', dateOfBirth: '', responsible: '',
  visitDate: '', professional: ''
};

const initialAssessment: AssessmentData = {
  domains: {
    reception: { reaction: '', adaptation: '', responseToNewPeople: '', supportNeeds: '', curiosity: '' },
    communication: { type: '', responseToName: '', initiates: '', simpleInstructions: '', complexInstructions: '', functional: '' },
    behavior: { anxiety: '', stereotypies: '', autoRegulation: '', frustration: '', flexibility: '' },
    social: { peerSearch: '', approximation: '', sharing: '', eyeContact: '', collective: '' },
    sensory: { soundReaction: '', lightSensitivity: '', seeking: '', avoidance: '', tolerance: '' },
    academic: { interest: '', jointAttention: '', sustainedAttention: '', instructions: '', preAcademic: '' },
    dailyLife: { bathroom: '', feeding: '', organization: '', transitions: '' }
  },
  strengths: '',
  challenges: '',
  recommendations: '',
  generalOpinion: ''
};

const initialConfig: ReportConfig = {
  tone: 'formal'
};

function App() {
  const [currentStep, setCurrentStep] = useState<Step>(Step.STUDENT_INFO);
  const [studentData, setStudentData] = useState<StudentInfo>(initialStudent);
  const [assessmentData, setAssessmentData] = useState<AssessmentData>(initialAssessment);
  const [config, setConfig] = useState<ReportConfig>(initialConfig);
  
  const [generatedReport, setGeneratedReport] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    setIsLoading(true);
    try {
      const fullData: ReportData = {
        student: studentData,
        assessment: assessmentData,
        config: config
      };
      const result = await generateReport(fullData);
      setGeneratedReport(result);
      setCurrentStep(Step.RESULT);
    } catch (error) {
      alert("Houve um erro ao gerar o relatório. Verifique sua conexão ou tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFillExample = () => {
    const today = new Date().toISOString().split('T')[0];
    
    setStudentData({
      name: 'Lucas Oliveira',
      age: '7 anos',
      grade: '1º Ano do Ensino Fundamental',
      school: 'Escola Municipal Estrela do Saber',
      dateOfBirth: '2017-04-12',
      responsible: 'Ana Oliveira (Mãe)',
      visitDate: today,
      professional: 'Dra. Mariana Santos (Neuropsicopedagoga)'
    });

    setAssessmentData({
      domains: {
        reception: {
          reaction: 'Entrou com cautela, segurando a mão da mãe. Evitou olhar para os inspetores no portão.',
          adaptation: 'Levou cerca de 15 minutos para soltar a mão da mãe. Aceitou entrar na sala após ver brinquedos de empilhar.',
          responseToNewPeople: 'Ignorou inicialmente. Aceitou interação apenas quando a professora ofereceu um objeto de interesse.',
          supportNeeds: 'Necessitou de mediação física leve para se direcionar à sala.',
          curiosity: 'Explorou visualmente os cartazes na parede, mas não tocou nos objetos sem permissão.'
        },
        communication: {
          type: 'Verbal, mas com frases curtas e objetivas.',
          responseToName: 'Respondeu em 3 das 5 tentativas. Melhor resposta quando o falante estava no campo visual.',
          initiates: 'Raramente inicia. Puxou a mão da professora para pedir água.',
          simpleInstructions: 'Compreende bem ("sente-se", "pegue o lápis").',
          complexInstructions: 'Dificuldade com comandos de duas etapas ("pegue o caderno e guarde na mochila"). Precisa de segmentação.',
          functional: 'Usa a fala principalmente para solicitações de necessidades básicas.'
        },
        behavior: {
          anxiety: 'Sinais de ansiedade (tapando ouvidos) durante o sinal do recreio.',
          stereotypies: 'Flapping de mãos (balançar) quando feliz ao conseguir montar o quebra-cabeça.',
          autoRegulation: 'Buscou um canto mais calmo da sala quando houve muito barulho.',
          frustration: 'Chorou brevemente quando não conseguiu abrir a lancheira, mas aceitou ajuda.',
          flexibility: 'Resistiu um pouco à troca de atividade (do parquinho para a sala), precisou de aviso prévio.'
        },
        social: {
          peerSearch: 'Não buscou ativamente outras crianças. Brincou em paralelo.',
          approximation: 'Aceitou quando um colega entregou uma peça, mas não manteve a interação.',
          sharing: 'Dificuldade em dividir os blocos de montar. Protegeu os objetos com o corpo.',
          eyeContact: 'Fugaz. Mantém por poucos segundos.',
          collective: 'Participou da roda de música, mas permaneceu sentado um pouco afastado do círculo.'
        },
        sensory: {
          soundReaction: 'Hipersensibilidade auditiva notada (sinal da escola, arrastar de cadeiras).',
          lightSensitivity: 'Não demonstrou desconforto com a iluminação da sala.',
          seeking: 'Busca texturas (passava a mão na parede rugosa do corredor).',
          avoidance: 'Evitou toques inesperados de outras crianças.',
          tolerance: 'Boa tolerância ao ambiente de sala de aula, desde que estruturado.'
        },
        academic: {
          interest: 'Grande interesse por números e letras magnéticas.',
          jointAttention: 'Apontou para mostrar um desenho que fez, buscando o olhar da professora.',
          sustainedAttention: 'Ficou 20 minutos focado na atividade de pareamento de cores.',
          instructions: 'Segue rotinas visuais melhor que verbais.',
          preAcademic: 'Reconhece cores, números até 20 e vogais. Segura o lápis com preensão palmar.'
        },
        dailyLife: {
          bathroom: 'Pediu para ir ao banheiro. Possui desfralde diurno, mas precisa de supervisão para higiene.',
          feeding: 'Comeu sozinho (lanche trazido de casa). Seletividade alimentar observada (apenas alimentos secos).',
          organization: 'Guardou o estojo quando solicitado.',
          transitions: 'Transição sala-pátio foi tranquila; pátio-sala gerou desorganização leve.'
        }
      },
      strengths: 'Boa memória visual, reconhecimento de letras e números, capacidade de atenção sustentada em atividades de interesse, compreende regras visuais.',
      challenges: 'Hipersensibilidade auditiva, interação social com pares, flexibilidade cognitiva em mudanças de rotina, comunicação funcional para diálogos.',
      recommendations: 'Uso de fones abafadores em momentos de ruído intenso. Uso de rotina visual (pistas visuais) para antecipar transições. Atividades que estimulem a troca de turnos e compartilhamento. Mediação nas interações sociais no recreio.',
      generalOpinion: 'O aluno demonstra potencial acadêmico preservado, com desafios típicos do espectro nas áreas de comunicação social e sensorial. A adaptação ao ambiente escolar é positiva, desde que respeitadas suas necessidades de regulação sensorial e previsibilidade.'
    });
  };

  const resetApp = () => {
    setStudentData(initialStudent);
    setAssessmentData(initialAssessment);
    setGeneratedReport(null);
    setCurrentStep(Step.STUDENT_INFO);
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-20">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 py-4 no-print">
        <div className="max-w-5xl mx-auto px-4 flex items-center gap-3">
          <div className="bg-indigo-600 p-2 rounded-lg">
            <Brain className="text-white" size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800">PsicoRelat.io</h1>
            <p className="text-xs text-slate-500">Instrumento de Avaliação da Visita Escolar - TEA</p>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <div className="no-print">
        <Steps currentStep={currentStep} setStep={setCurrentStep} />
      </div>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 mt-6">
        {currentStep === Step.STUDENT_INFO && (
          <StudentForm 
            data={studentData} 
            updateData={(d) => setStudentData(prev => ({...prev, ...d}))} 
            onNext={() => setCurrentStep(Step.ASSESSMENT)} 
            onFillExample={handleFillExample}
          />
        )}

        {currentStep === Step.ASSESSMENT && (
          <AssessmentForm 
            data={assessmentData} 
            updateData={(d) => setAssessmentData(prev => ({...prev, ...d}))}
            onNext={() => setCurrentStep(Step.ANALYSIS)}
            onBack={() => setCurrentStep(Step.STUDENT_INFO)}
          />
        )}

        {currentStep === Step.ANALYSIS && (
          <AnalysisForm 
            data={assessmentData}
            config={config}
            updateData={(d) => setAssessmentData(prev => ({...prev, ...d}))}
            updateConfig={(c) => setConfig(prev => ({...prev, ...c}))}
            onBack={() => setCurrentStep(Step.ASSESSMENT)}
            onGenerate={handleGenerate}
            isLoading={isLoading}
          />
        )}

        {currentStep === Step.RESULT && generatedReport && (
          <ReportResult 
            content={generatedReport} 
            onReset={resetApp} 
          />
        )}
      </main>
    </div>
  );
}

export default App;