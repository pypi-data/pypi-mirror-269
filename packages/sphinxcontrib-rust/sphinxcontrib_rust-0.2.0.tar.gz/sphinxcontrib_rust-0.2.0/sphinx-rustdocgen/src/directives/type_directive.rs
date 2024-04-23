//! Implementation of the ``rust:type::`` directive

use quote::quote;
use syn::{ImplItemType, ItemType, TraitItemType, Visibility};

use crate::check_visibility;
use crate::directives::{extract_doc_from_attrs, Directive, DirectiveOption, DirectiveVisibility};
use crate::formats::{MdContent, MdDirective, RstContent, RstDirective};

#[derive(Clone, Debug)]
pub(crate) struct TypeDirective {
    pub(crate) name: String,
    pub(crate) options: Vec<DirectiveOption>,
    pub(crate) content: Vec<String>,
}

macro_rules! type_from_item {
    ($parent_path:expr, $item:expr, $vis:expr, $inherited:expr) => {{
        let name = format!("{}::{}", $parent_path, &$item.ident);

        let ident = &$item.ident;
        let (_, ty, wc) = $item.generics.split_for_impl();
        let options = vec![
            DirectiveOption::Vis(DirectiveVisibility::effective_visibility(&$vis, $inherited)),
            DirectiveOption::Sig(quote! {type #ident #ty #wc}.to_string()),
        ];

        Directive::Type(TypeDirective {
            name,
            options,
            content: extract_doc_from_attrs(&$item.attrs),
        })
    }};
}

impl TypeDirective {
    pub(crate) fn from_item(
        parent_path: &str,
        item: &ItemType,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        type_from_item!(parent_path, item, item.vis, inherited_visibility)
    }

    pub(crate) fn from_impl_item(
        parent_path: &str,
        item: &ImplItemType,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        type_from_item!(parent_path, item, item.vis, inherited_visibility)
    }

    pub(crate) fn from_trait_item(
        parent_path: &str,
        item: &TraitItemType,
        inherited_visibility: &Option<&Visibility>,
    ) -> Directive {
        type_from_item!(
            parent_path,
            item,
            Visibility::Inherited,
            inherited_visibility
        )
    }
}

impl RstDirective for TypeDirective {
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let content_indent = Self::make_content_indent(level);

        let mut text = Self::make_rst_header("type", &self.name, &self.options, level);
        text.extend(self.content.get_rst_text(&content_indent));

        text
    }
}

impl MdDirective for TypeDirective {
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String> {
        check_visibility!(self.options, max_visibility);
        let fence = Self::make_fence(fence_size);

        let mut text = Self::make_md_header("type", &self.name, &self.options, &fence);
        text.extend(self.content.get_md_text());

        text.push(fence);
        text
    }
}
