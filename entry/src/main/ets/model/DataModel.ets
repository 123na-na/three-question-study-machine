export interface Course {
  id: number;
  name: string;
  description: string;
  is_sample: boolean;
  created_at: string;
}

export interface KnowledgePoint {
  id: number;
  course_id: number;
  title: string;
  content: string;
  created_at: string;
}

export interface LearningSession {
  id: number;
  knowledge_point_id: number;
  step: string;
  status: string;
  started_at: string;
  completed_at?: string;
  score: number;
}

export interface DialogueRecord {
  id: number;
  session_id: number;
  turn_index: number;
  user_input: string;
  ai_response: string;
  timestamp: string;
}

export interface AIEvaluationResponse {
  score: number;
  feedback: string;
  follow_up_question: string;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlocked_at: string;
}

export interface Certificate {
  course_id: number;
  course_name: string;
  completed_kp: number;
  total_kp: number;
  avg_score: number;
  completed_at: string;
}

export interface ReviewRecord {
  id: number;
  knowledge_point_id: number;
  ease_factor: number;
  interval_days: number;
  next_review_date: string;
  last_reviewed_at: string;
  review_count: number;
  avg_score: number;
  status: string;
}
