# ArgoCD 설치 가이드 (argocd 네임스페이스)

## 1) 네임스페이스 생성
```bash
kubectl apply -f k8s/argocd/namespace.yaml
```

## 2) ArgoCD 설치
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## 3) NodePort로 ArgoCD 서버 노출
```bash
kubectl -n argocd patch svc argocd-server -p '{"spec": {"type": "NodePort"}}'
```

## 4) 관리자 초기 비밀번호 확인
```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo
```

## 5) 접근 제한 (권장)
허용된 IP만 접근할 수 있도록 보안 그룹에서 NodePort를 제한하세요.
