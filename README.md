# Namespace with deletion protection

This directory contains a Kubernetes Namespace manifest and a
`ValidatingAdmissionPolicy` that denies deletion of that namespace. The policy
and its binding are included in the generated YAML.

## Generate the manifests

Run the generator with a namespace name:

```sh
python3 generate.py my-namespace
```

By default, this writes `namespace-protection.yaml` in this directory. To write
to a different path, use `-o`:

```sh
python3 generate.py my-namespace -o output/my-namespace.yaml
```

The name must be a lowercase Kubernetes DNS label, up to 63 characters.

## Apply

```sh
kubectl apply -f namespace-protection.yaml
```

The cluster must support `admissionregistration.k8s.io/v1`
`ValidatingAdmissionPolicy` resources. The policy rejects Namespace deletion
for the generated namespace. A cluster administrator can still remove or
change the policy or its binding.
# kustom-namespace
