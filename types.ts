export interface StudentInfo {
  name: string;
  age: string;
  grade: string;
  school: string;
  dateOfBirth: string;
  responsible: string;
  visitDate: string; // New field from PDF
  professional: string; // New field from PDF
}

export interface ObservationDomains {
  reception: {
    reaction: string;
    adaptation: string;
    responseToNewPeople: string;
    supportNeeds: string;
    curiosity: string;
  };
  communication: {
    type: string;
    responseToName: string;
    initiates: string;
    simpleInstructions: string;
    complexInstructions: string;
    functional: string;
  };
  behavior: {
    anxiety: string;
    stereotypies: string;
    autoRegulation: string;
    frustration: string;
    flexibility: string;
  };
  social: {
    peerSearch: string;
    approximation: string;
    sharing: string;
    eyeContact: string;
    collective: string;
  };
  sensory: {
    soundReaction: string;
    lightSensitivity: string;
    seeking: string;
    avoidance: string;
    tolerance: string;
  };
  academic: {
    interest: string;
    jointAttention: string;
    sustainedAttention: string;
    instructions: string;
    preAcademic: string;
  };
  dailyLife: {
    bathroom: string;
    feeding: string;
    organization: string;
    transitions: string;
  };
}

export interface AssessmentData {
  domains: ObservationDomains;
  strengths: string; // Pontos Fortes
  challenges: string; // Desafios Identificados
  recommendations: string; // Recomendações
  generalOpinion: string; // Parecer Geral
}

export interface ReportConfig {
  tone: 'formal' | 'objective' | 'explanatory';
}

export interface ReportData {
  student: StudentInfo;
  assessment: AssessmentData;
  config: ReportConfig;
}

export enum Step {
  STUDENT_INFO = 0,
  ASSESSMENT = 1,
  ANALYSIS = 2,
  RESULT = 3,
}