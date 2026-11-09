import { getPreference, setPreference } from './DatabaseHelper';

export async function getNickname(): Promise<string | null> {
  return await getPreference('nickname');
}

export async function setNickname(name: string): Promise<void> {
  await setPreference('nickname', name);
}

export async function getUserId(): Promise<string | null> {
  let uid = await getPreference('user_id');
  if (!uid) {
    uid = 'user_' + Date.now().toString(36) + Math.random().toString(36).substring(2, 8);
    await setPreference('user_id', uid);
  }
  return uid;
}

export async function isLoggedIn(): Promise<boolean> {
  const name = await getNickname();
  return name !== null && name.length > 0;
}
